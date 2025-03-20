from modelengine_agents.agent_en.tools import Tool
import requests
from exa_py import Exa


class EXASearchTool(Tool):
    name = "exa_web_search"
    description = "Performs a EXA web search based on your query (think a Google search) then returns the top search results."
    inputs = {"query": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"


    def __init__(self, exa_api_key, max_results=5, is_model_summary=False):
        super().__init__()

        self.exa = Exa(api_key=exa_api_key)
        self.max_results = max_results
        self.is_model_summary = is_model_summary


    def forward(self, query: str) -> str:

        if self.is_model_summary:
            summary_prompt = f"请总结以下网页的主要内容，提取关键信息，并回答用户的问题。确保总结简洁明了，涵盖核心观点、数据和结论。如果网页内容涉及多个主题，请分别概述每个主题的重点。用户的问题是：[{query}]。请根据网页内容提供准确的回答，并注明信息来源（如适用）。"

            exa_search_result = self.exa.search_and_contents(
                query,
                text=True,
                num_results=self.max_results,
                summary={
                    "query":summary_prompt
                }
            )
        else:
            exa_search_result = self.exa.search_and_contents(
                query,
                text=True,
                num_results=self.max_results
            )

        if len(exa_search_result.results) == 0:
            raise Exception("No results found! Try a less restrictive/shorter query.")

        processed_results = [f"[{result.title}]\n{result.text}" for result in exa_search_result.results]

        return "## Search Results\n\n" + "\n\n".join(processed_results)
