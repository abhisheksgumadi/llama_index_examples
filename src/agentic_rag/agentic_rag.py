import asyncio
from llama_index.readers.file import UnstructuredReader
from llama_index.llms.ollama import Ollama
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core import (
    VectorStoreIndex,
)
from llama_index.core.objects import ObjectIndex
from llama_index.postprocessor.cohere_rerank import CohereRerank
from agentic_rag.document_loader import DocumentLoader
from agentic_rag.llm_config import LLMConfig
from agentic_rag.document_agent_builder import DocumentAgentBuilder
from agentic_rag.agent_tool_builder import AgentToolBuilder
from agentic_rag.top_agent_builder import CustomObjectRetriever


async def main():
    llm_config = LLMConfig()

    # Load documents
    # Load documents and create agents
    doc_loader = DocumentLoader()
    docs = doc_loader.load_documents()

    # Build document agents
    doc_agent_builder = DocumentAgentBuilder(llm_config)
    agents_dict, extra_info_dict = await doc_agent_builder.build_agents(docs)

    # Create tools from document agents
    tool_builder = AgentToolBuilder(agents_dict, extra_info_dict)
    all_tools = tool_builder.build_tools()

    # Create object index
    obj_index = ObjectIndex.from_objects(
        all_tools,
        index_cls=VectorStoreIndex,
    )

    # Create vector node retriever
    vector_node_retriever = obj_index.as_node_retriever(
        similarity_top_k=10,
    )

    # Wrap it with ObjectRetriever to return objects
    custom_obj_retriever = CustomObjectRetriever(
        vector_node_retriever,
        obj_index.object_node_mapping,
        node_postprocessors=[CohereRerank(top_n=5, model="rerank-v3.5")],
        llm=llm_config.llm,
    )

    # Build top agent
    top_agent = ReActAgent(
        tool_retriever=custom_obj_retriever,
        system_prompt=""" \
                    You are an agent designed to answer queries about the documentation.
                    Please always use the tools provided to answer a question. Do not rely on prior knowledge.\

                    """,
        llm=llm_config.llm,
    )

    # Run top agent
    handler = await top_agent.run(
        "How many developers use the Nvidia Jetson platform?",
    )
    print(handler)


if __name__ == "__main__":
    asyncio.run(main())
