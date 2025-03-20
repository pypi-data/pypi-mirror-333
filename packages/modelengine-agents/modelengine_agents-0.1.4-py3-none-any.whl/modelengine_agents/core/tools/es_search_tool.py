from modelengine_agents.agent_en.tools import Tool


class ESSearchTool(Tool):

    name = "es_search"
    description = "Performs Elasticsearch search based on your query then returns the top search results."
    inputs = {"answer": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"

    def __init__(self):
        super().__init__()

        # 连接到 es 服务器


    def forward(self, query: str) -> str:
        # 传入问题，输出es检索的字符串
        return ""
