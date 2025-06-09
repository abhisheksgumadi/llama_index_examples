from llama_index.core.tools import FunctionTool
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.objects import ObjectRetriever
from llama_index.core.schema import QueryBundle


# define a custom object retriever that adds in a query planning tool
class CustomObjectRetriever(ObjectRetriever):
    def __init__(
        self,
        retriever,
        object_node_mapping,
        node_postprocessors=None,
        llm=None,
    ):
        self._retriever = retriever
        self._object_node_mapping = object_node_mapping
        self._llm = llm
        self._node_postprocessors = node_postprocessors or []

    def retrieve(self, query_bundle):
        if isinstance(query_bundle, str):
            query_bundle = QueryBundle(query_str=query_bundle)

        nodes = self._retriever.retrieve(query_bundle)
        for processor in self._node_postprocessors:
            nodes = processor.postprocess_nodes(nodes, query_bundle=query_bundle)
        tools = [self._object_node_mapping.from_node(n.node) for n in nodes]

        sub_agent = FunctionAgent(
            name="compare_tool",
            description=f"""\
            Useful for any queries that involve comparing multiple documents. ALWAYS use this tool for comparison queries - make sure to call this \
            tool with the original query. Do NOT use the other tools for any queries involving multiple documents.
            """,
            tools=tools,
            llm=self._llm,
            system_prompt="""You are an expert at comparing documents. Given a query, use the tools provided to compare the documents and return a summary of the results.""",
        )

        async def query_sub_agent(query: str) -> str:
            response = await sub_agent.run(query)
            return str(response)

        sub_question_tool = FunctionTool.from_defaults(
            query_sub_agent,
            name=sub_agent.name,
            description=sub_agent.description,
        )
        return tools + [sub_question_tool]
