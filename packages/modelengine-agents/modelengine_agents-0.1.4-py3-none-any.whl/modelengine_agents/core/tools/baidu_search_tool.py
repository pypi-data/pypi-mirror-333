from modelengine_agents.agent_en.tools import Tool
import requests
from baidusearch.baidusearch import search
from bs4 import BeautifulSoup
import re


class BaiduSearchTool(Tool):
    name = "baidu_web_search"
    description = "Performs a baidu web search based on your query (think a Google search) then returns the top search results."
    inputs = {"query": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"


    def __init__(self, max_results=10):
        super().__init__()
        self.max_result = max_results


    def forward(self, query: str) -> str:
        baidu_results = search(query, num_results=self.max_result)
        records = [{
            "title": str_clean(result["title"]),
            "abstract": str_clean(result["abstract"]),
            "text": parse_url(result["url"])
        } for result in baidu_results]

        processed_results = [f"[{record['title']}]\n{record['abstract']}\n{record['text']}" for record in records]
        return "## Search Results\n\n" + "\n\n".join(processed_results)


def parse_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code ==200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            text = soup.text
            return str_clean(text)
        else:
            return ""
    except:
        return ""


def str_clean(input_str):
    # 去除html标签
    input_str = re.sub(r"<[^>]+>", "", input_str)
    # 只保留中英文与标点符号
    input_str = re.sub(r"[^\x00-\x7E\u4e00-\u9fa5]", "", input_str)
    # 去除多余空格以及换行，全部替换成空格
    input_str = re.sub(r"\s+", " ", input_str)
    return input_str
