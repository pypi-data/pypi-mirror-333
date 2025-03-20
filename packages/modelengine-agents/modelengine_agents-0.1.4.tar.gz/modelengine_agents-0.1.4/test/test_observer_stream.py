
from modelengine_agents.core.models.LiteLLMModelME import LiteLLMModelME
from modelengine_agents.agent_en.default_tools import DuckDuckGoSearchTool, GoogleSearchTool
from modelengine_agents.core.models.OpenAIServerModelME import OpenAIServerModelME
from modelengine_agents.core.observer.observer import MessageObserver
from modelengine_agents.core.agents.CodeAgentME import CodeAgentME
from modelengine_agents.core.tools.exa_search_tool import EXASearchTool
from modelengine_agents.core.tools.baidu_search_tool import BaiduSearchTool
from modelengine_agents.core.tools.google_search_tool import GoogleSearchTool
from modelengine_agents.core.tools.final_answer_format_tool import FinalAnswerFormatTool
from modelengine_agents.core.agents.ToolCallingAgentME import ToolCallingAgentME


"""
description: 单独测试,从控制台获取agent.run运行结果
"""


def single_agent():
    observer = MessageObserver()

    model = OpenAIServerModelME(
        observer=observer,
        model_id="deepseek-ai/DeepSeek-V3",
        api_key="sk-",
        api_base="https://api.siliconflow.cn")

    search_tool = BaiduSearchTool(max_results= 6)

    system_prompt = "针对用户提问问题，从检索内容中提取有关信息进行总结。要求有标题与正文内容。"
    final_answer_tool = FinalAnswerFormatTool(llm=model, system_prompt=system_prompt)

    search_request_agent = CodeAgentME(
        observer=observer,
        tools=[search_tool, final_answer_tool],
        model=model,
        name="smart_agent",
        max_steps=5
    )

    # search_request_agent.run("介绍华为汽车")
    search_request_agent.run("特朗普内阁成员")


def multi_agent():
    observer = MessageObserver()
    model = LiteLLMModelME(
        observer=observer,
        model_id="deepseek/deepseek-chat",
        api_key="sk-",
        api_base="https://api.deepseek.com")

    search_request_agent = CodeAgentME(
        observer=observer,
        tools=[DuckDuckGoSearchTool()],
        model=model,
        name="web_search_agent",
        description="Runs web searches for you. Give it your query as an argument.",
        max_steps=5
    )

    manager_agent = CodeAgentME(
        observer=observer,
        tools=[],
        model=model,
        name="manager_agent",
        managed_agents=[search_request_agent],
        max_steps=5
    )
    # manager_agent.run("对比DeepSeek和OpenAI的开源策略")
    manager_agent.run("特朗普内阁成员")


if __name__ == "__main__":
    single_agent()
    # multi_agent()
