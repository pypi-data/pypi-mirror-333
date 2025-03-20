from pymilvus import connections


from modelengine_agents.agent_en.tools import Tool


class MilvusSearchTool(Tool):

    name = "milvus_search"
    description = "Performs a milvus vector database search based on your query then returns the top search results."
    inputs = {"answer": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"

    def __init__(self):
        super().__init__()

        # 连接到 Milvus 服务器
        connections.connect("default", host="localhost", port="19530")

    def forward(self, query: str) -> str:
        # 传入问题，输出milvus检索的字符串
        return ""



