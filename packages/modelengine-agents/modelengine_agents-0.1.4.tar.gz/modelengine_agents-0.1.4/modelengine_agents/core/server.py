import json
from typing import Optional
import re

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import time
import uvicorn
from threading import Thread

from starlette.exceptions import HTTPException


from modelengine_agents.agent_en.memory import MemoryStep

from modelengine_agents.agent_en import handle_agent_output_types, AgentText, DuckDuckGoSearchTool, ActionStep
from modelengine_agents.core import CodeAgentME, LiteLLMModelME, OpenAIServerModelME, MessageObserver, BaiduSearchTool, FinalAnswerFormatTool


def pull_messages_from_step(
    step_log: MemoryStep,
):
    """Extract ChatMessage objects from agent steps with proper nesting"""
    import gradio as gr

    if isinstance(step_log, ActionStep):
        # # Output the step number
        step_number = f"Step {step_log.step_number}" if step_log.step_number is not None else ""

        # For tool calls, create a parent message
        if hasattr(step_log, "tool_calls") and step_log.tool_calls is not None:
            first_tool_call = step_log.tool_calls[0]
            used_code = first_tool_call.name == "python_interpreter"
            parent_id = f"call_{len(step_log.tool_calls)}"

            # Tool call becomes the parent message with timing info
            # First we will handle arguments based on type
            args = first_tool_call.arguments
            if isinstance(args, dict):
                content = str(args.get("answer", str(args)))
            else:
                content = str(args).strip()

            if used_code:
                # Clean up the content by removing any end code tags
                content = re.sub(r"```.*?\n", "", content)  # Remove existing code blocks
                content = re.sub(r"\s*<end_code>\s*", "", content)  # Remove end_code tags
                content = content.strip()
                if not content.startswith("```python"):
                    content = f"```python\n{content}\n```"

            parent_message_tool = gr.ChatMessage(
                role="assistant",
                content=content,
                metadata={
                    "title": f"🛠️ Used tool {first_tool_call.name}",
                    "id": parent_id,
                    "status": "pending",
                },
            )
            # 此处不返回，已经通过observer获取到了
            # yield parent_message_tool

            # Nesting execution logs under the tool call if they exist
            if hasattr(step_log, "observations") and (
                step_log.observations is not None and step_log.observations.strip()
            ):  # Only yield execution logs if there's actual content
                log_content = step_log.observations.strip()
                if log_content:
                    log_content = re.sub(r"^Execution logs:\s*", "", log_content)
                    # yield gr.ChatMessage(
                    #     role="assistant",
                    #     content=f"```bash\n{log_content}\n```\n",
                    #     metadata={"title": "📝 Execution Logs", "parent_id": parent_id, "status": "done"},
                    # )

            # Nesting any errors under the tool call
            if hasattr(step_log, "error") and step_log.error is not None:
                yield gr.ChatMessage(
                    role="assistant",
                    content=str(step_log.error),
                    metadata={"title": "💥 Error", "parent_id": parent_id, "status": "done"},
                )

            # Update parent message metadata to done status without yielding a new message
            parent_message_tool.metadata["status"] = "done"

        # Handle standalone errors but not from tool calls
        elif hasattr(step_log, "error") and step_log.error is not None:
            yield gr.ChatMessage(role="assistant", content=str(step_log.error), metadata={"title": "💥 Error"})

        # Calculate duration and token information
        step_footnote = f"{step_number}"
        if hasattr(step_log, "input_token_count") and hasattr(step_log, "output_token_count"):
            token_str = (
                f" | Input-tokens:{step_log.input_token_count:,} | Output-tokens:{step_log.output_token_count:,}"
            )
            step_footnote += token_str
        if hasattr(step_log, "duration"):
            step_duration = f" | Duration: {round(float(step_log.duration), 2)}" if step_log.duration else None
            step_footnote += step_duration
        step_footnote = f"""<span style="color: #bbbbc2; font-size: 12px;">{step_footnote}</span> """
        yield gr.ChatMessage(role="assistant", content=f"{step_footnote}")
        yield gr.ChatMessage(role="assistant", content="-----", metadata={"status": "done"})


def agent_run_thread(agent: CodeAgentME, query: str):
    total_input_tokens, total_output_tokens = 0, 0
    observer = agent.observer
    try:
        for step_log in agent.run(query, stream=True):
            if getattr(agent.model, "last_input_token_count", None) is not None:
                total_input_tokens += agent.model.last_input_token_count
                total_output_tokens += agent.model.last_output_token_count
                if isinstance(step_log, ActionStep):
                    step_log.input_token_count = agent.model.last_input_token_count
                    step_log.output_token_count = agent.model.last_output_token_count

            for message in pull_messages_from_step(
                    step_log,
            ):
                if message is not None:
                    # message 为gr.message
                    title = message.metadata.get("title", "")
                    content = message.content
                    output_str = f"\n{title}\n{content}\n"

                    observer.add_new_data(output_str)

        final_answer = step_log  # Last log is the run's final_answer
        final_answer = handle_agent_output_types(final_answer)

        if isinstance(final_answer, AgentText):
            observer.add_new_data(f"**Final answer:**\n{final_answer.to_string()}\n")
        else:
            observer.add_new_data(f"**Final answer:** {str(final_answer)}\n")
    except Exception as e:
        print(f"Error in interaction: {str(e)}")
        observer.add_new_data(f"Error in interaction: {str(e)}")


def agent_run(agent: CodeAgentME, query: str):
    if not isinstance(agent, CodeAgentME):
        raise HTTPException(status_code=400, detail="Create Agent Object with CodeAgentME")
    if not isinstance(agent.model, (LiteLLMModelME, OpenAIServerModelME)):
        raise HTTPException(status_code=400, detail="Create Model Object with LiteLLMModelME")
    if not isinstance(agent.observer, MessageObserver):
        raise HTTPException(status_code=400, detail="Create Observer Object with MessageObserver")

    observer = agent.observer

    # 目前已知的遗留问题，当前端主动中断后，该线程不会停止，仍会执行
    thread_agent = Thread(target=agent_run_thread, args=(agent, query))
    thread_agent.start()

    while thread_agent.is_alive():
        output_str =  observer.get_output_str()
        if len(output_str):
            yield output_str

        time.sleep(0.2)

    yield observer.get_output_str()


# 创建server，需要在这里构建自己的Agent
def create_single_agent():
    observer = MessageObserver()
    # model和Agent必须使用同一个observer

    model = OpenAIServerModelME(
        observer=observer,
        model_id="deepseek-ai/DeepSeek-V3",
        api_key="sk-",
        api_base="https://api.siliconflow.cn")

    system_prompt = "针对用户提问问题，从检索内容中提取有关信息进行总结。要求有标题与正文内容。"
    final_answer_tool = FinalAnswerFormatTool(llm=model, system_prompt=system_prompt)

    search_request_agent = CodeAgentME(
        observer=observer,
        tools=[BaiduSearchTool(max_results=6), final_answer_tool],
        model=model,
        name="web_search_agent"
    )

    return search_request_agent


def create_mul_agent():
    observer = MessageObserver()

    model = OpenAIServerModelME(
        observer=observer,
        model_id="deepseek-ai/DeepSeek-V3",
        api_key="sk-",
        api_base="https://api.siliconflow.cn")


    search_request_agent = CodeAgentME(
        observer=observer,
        tools=[BaiduSearchTool(max_results=6)],
        model=model,
        name="web_search_agent",
        description="Runs web searches for you. Give it your query as an argument.",
        max_steps=5
    )

    system_prompt = "针对用户提问问题，从检索内容中提取有关信息进行总结。要求有标题与正文内容。"
    final_answer_tool = FinalAnswerFormatTool(llm=model, system_prompt=system_prompt)
    manager_agent = CodeAgentME(
        observer=observer,
        tools=[final_answer_tool],
        model=model,
        name="manager_agent",
        managed_agents=[search_request_agent],
        max_steps=5
    )
    return manager_agent



app = FastAPI()

class FrontQuery(BaseModel):
    query: str


@app.post(path='/single_agent', summary="这是一个测试agent")
async def single_agent(request: FrontQuery):
    try:
        query = request.query
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        # agent = create_single_agent()
        agent = create_mul_agent()
    except Exception as e:
        raise HTTPException(status_code=400, detail="ERROR IN: create agent! Exception:" + str(e))

    return StreamingResponse(agent_run(agent, query), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)