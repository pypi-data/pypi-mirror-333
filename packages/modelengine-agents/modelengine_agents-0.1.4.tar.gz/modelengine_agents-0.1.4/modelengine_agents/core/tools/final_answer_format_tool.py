from typing import Any
from modelengine_agents.agent_en.tools import Tool
from modelengine_agents.agent_en.models import MessageRole


class FinalAnswerFormatTool(Tool):
    name = "summary_tool"
    description = "针对用户提问问题，从检索内容中提取有关信息进行总结。可以直接传入检索结果的变量名。返回内容可以作为问题的最终回答。"
    inputs = {"query": {"type": "string", "description": "输入用户提问"},
              "search_result": {"type": "string", "description": "输入检索到的信息，可以直接传入之前检索的字符串变量"}}
    output_type = "string"

    def __init__(self, llm, system_prompt):
        super().__init__()
        self.model = llm
        self.system_prompt = system_prompt

    def forward(self, query: str, search_result: str) -> str:
        messages = [
            {"role": MessageRole.SYSTEM, "content": self.system_prompt},
            {"role": MessageRole.USER, "content": f"### 检索信息：{search_result}\n### 用户提问：{query}\n"}
        ]
        model_output_message = self.model(messages=messages,
                                          temperature=0.6)

        return model_output_message.content
