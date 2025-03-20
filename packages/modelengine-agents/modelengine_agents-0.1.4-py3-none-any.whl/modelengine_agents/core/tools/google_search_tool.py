from modelengine_agents.agent_en.tools import Tool
import requests
from googlesearch import search
from bs4 import BeautifulSoup
import re
from modelengine_agents.core.tools.baidu_search_tool import parse_url, str_clean


class GoogleSearchTool(Tool):
    name = "google_web_search"
    description = "Performs a google web search based on your query then returns the top search results."
    inputs = {"query": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"


    def __init__(self, max_results=10):
        super().__init__()
        self.max_result = max_results


    def forward(self, query: str) -> str:
        google_results = []
        for result in search(query, num_results=10, advanced=True):
            google_results.append(result)

        records = [{
            "title": str_clean(result.title),
            "description": str_clean(result.description),
            "text": str_clean(parse_url(result.url))
        } for result in google_results]

        processed_results = [f"[{record['title']}]\n{record['description']}\n{record['text']}" for record in records]
        return "## Search Results\n\n" + "\n\n".join(processed_results)

