from typing import Union, Any
from rich.text import Text
from rich.panel import Panel

from modelengine_agents.agent_en import AgentImage, AgentAudio, ActionStep, ToolCallingAgent, AgentGenerationError, ChatMessage, ToolCall, LogLevel
from modelengine_agents.core import MessageObserver, ProcessType

import yaml

import os


YELLOW_HEX = "#d4b702"

class ToolCallingAgentME(ToolCallingAgent):
    def __init__(self, observer: MessageObserver, lang="zh", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.observer = observer

        self.lang = lang
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        # 根据语言重新确定prompt
        if lang=="zh":
            prompt_path = os.path.normpath(os.path.join(file_path, "../prompts/zh/toolcalling_agent.yaml"))
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.prompt_templates = yaml.safe_load(f)
        elif lang=="en":
            prompt_path = os.path.normpath(os.path.join(file_path, "../prompts/en/toolcalling_agent.yaml"))
            with open(prompt_path, "r") as f:
                self.prompt_templates = yaml.safe_load(f)


    def step(self, memory_step: ActionStep) -> Union[None, Any]:
        """
        Perform one step in the ReAct framework: the agent thinks, acts, and observes the result.
        Returns None if the step is not final.
        """
        self.observer.add_message(self.agent_name, ProcessType.STEP_COUNT, self.step_number)
        memory_messages = self.write_memory_to_messages()

        self.input_messages = memory_messages

        # Add new step in logs
        memory_step.model_input_messages = memory_messages.copy()

        try:
            model_message: ChatMessage = self.model(
                memory_messages,
                tools_to_call_from=list(self.tools.values()),
                stop_sequences=["Observation:"],
            )
            memory_step.model_output_message = model_message
            if model_message.tool_calls is None or len(model_message.tool_calls) == 0:
                raise Exception("Model did not call any tools. Call `final_answer` tool to return a final answer.")
            tool_call = model_message.tool_calls[0]
            tool_name, tool_call_id = tool_call.function.name, tool_call.id
            tool_arguments = tool_call.function.arguments

        except Exception as e:
            raise AgentGenerationError(f"Error in generating tool call with model:\n{e}", self.logger) from e

        # 记录大模型输出
        self.observer.add_message(self.agent_name, ProcessType.MODEL_OUTPUT, model_message.content)

        memory_step.tool_calls = [ToolCall(name=tool_name, arguments=tool_arguments, id=tool_call_id)]

        # Execute
        self.logger.log(
            Panel(Text(f"Calling tool: '{tool_name}' with arguments: {tool_arguments}")),
            level=LogLevel.INFO,
        )


        if tool_name == "final_answer":
            if isinstance(tool_arguments, dict):
                if "answer" in tool_arguments:
                    answer = tool_arguments["answer"]
                else:
                    answer = tool_arguments
            else:
                answer = tool_arguments
            if (
                isinstance(answer, str) and answer in self.state.keys()
            ):  # if the answer is a state variable, return the value
                final_answer = self.state[answer]
                self.logger.log(
                    f"[bold {YELLOW_HEX}]Final answer:[/bold {YELLOW_HEX}] Extracting key '{answer}' from state to return value '{final_answer}'.",
                    level=LogLevel.INFO,
                )
            else:
                final_answer = answer
                self.logger.log(
                    Text(f"Final answer: {final_answer}", style=f"bold {YELLOW_HEX}"),
                    level=LogLevel.INFO,
                )
            # 记录运行结果
            self.observer.add_message(self.agent_name, ProcessType.EXECUTION_LOGS, final_answer)

            memory_step.action_output = final_answer
            return final_answer
        else:
            if tool_arguments is None:
                tool_arguments = {}
            observation = self.execute_tool_call(tool_name, tool_arguments)
            observation_type = type(observation)
            if observation_type in [AgentImage, AgentAudio]:
                if observation_type == AgentImage:
                    observation_name = "image.png"
                elif observation_type == AgentAudio:
                    observation_name = "audio.mp3"
                # TODO: observation naming could allow for different names of same type

                self.state[observation_name] = observation
                updated_information = f"Stored '{observation_name}' in memory."
            else:
                updated_information = str(observation).strip()

            # 记录运行结果
            self.observer.add_message(self.agent_name, ProcessType.EXECUTION_LOGS, updated_information.replace('[', '|'))

            self.logger.log(
                f"Observations: {updated_information.replace('[', '|')}",  # escape potential rich-tag-like components
                level=LogLevel.INFO,
            )
            memory_step.observations = updated_information
            return None