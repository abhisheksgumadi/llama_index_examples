import asyncio
import os
import pickle
from pathlib import Path
from typing import Dict, List
from tqdm import tqdm

from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import (
    load_index_from_storage,
    StorageContext,
    VectorStoreIndex,
    SummaryIndex,
)
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent.workflow import FunctionAgent
from agentic_rag.llm_config import LLMConfig


class DocumentAgentBuilder:
    def __init__(self, llm_config: LLMConfig):
        self.llm = llm_config.llm
        self.node_parser = SentenceSplitter()

    async def build_agent_per_doc(
        self, nodes: List, file_base: str
    ) -> tuple[FunctionAgent, str]:
        vi_out_path = f"./data/index/{file_base}"
        summary_out_path = f"./data/index/{file_base}_summary.pkl"

        vector_index = self._get_or_create_vector_index(nodes, vi_out_path)
        summary_index = SummaryIndex(nodes)

        vector_query_engine = vector_index.as_query_engine(llm=self.llm)
        summary_query_engine = summary_index.as_query_engine(
            response_mode="tree_summarize", llm=self.llm
        )

        summary = await self._get_or_create_summary(
            summary_query_engine, summary_out_path
        )

        query_engine_tools = [
            QueryEngineTool.from_defaults(
                query_engine=vector_query_engine,
                name=f"vector_tool_{file_base}",
                description=f"Useful for questions related to specific facts",
            ),
            QueryEngineTool.from_defaults(
                query_engine=summary_query_engine,
                name=f"summary_tool_{file_base}",
                description=f"Useful for summarization questions",
            ),
        ]

        agent = FunctionAgent(
            tools=query_engine_tools,
            llm=self.llm,
            system_prompt=f"""\
You are a specialized agent designed to answer queries about the `{file_base}.pdf` part of company overview documents.
You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.\
""",
        )

        return agent, summary

    def _get_or_create_vector_index(
        self, nodes: List, vi_out_path: str
    ) -> VectorStoreIndex:
        if not os.path.exists(vi_out_path):
            Path("./data/index/").mkdir(parents=True, exist_ok=True)
            vector_index = VectorStoreIndex(nodes)
            vector_index.storage_context.persist(persist_dir=vi_out_path)
        else:
            vector_index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir=vi_out_path),
            )
        return vector_index

    async def _get_or_create_summary(
        self, summary_query_engine, summary_out_path: str
    ) -> str:
        if not os.path.exists(summary_out_path):
            Path(summary_out_path).parent.mkdir(parents=True, exist_ok=True)
            summary = str(
                await asyncio.wait_for(
                    summary_query_engine.aquery(
                        "Extract a concise 1-2 line summary of this document"
                    ),
                    timeout=600,
                )
            )
            print(summary)
            pickle.dump(summary, open(summary_out_path, "wb"))
        else:
            summary = pickle.load(open(summary_out_path, "rb"))
        return summary

    async def build_agents(self, docs: List[Document]) -> tuple[Dict, Dict]:
        agents_dict = {}
        extra_info_dict = {}

        for idx, doc in enumerate(tqdm(docs)):
            nodes = self.node_parser.get_nodes_from_documents([doc])
            file_path = Path(doc.metadata["path"])
            file_base = str(file_path.parent.stem) + "_" + str(file_path.stem)

            agent, summary = await self.build_agent_per_doc(nodes, file_base)
            agents_dict[file_base] = agent
            extra_info_dict[file_base] = {"summary": summary, "nodes": nodes}

        return agents_dict, extra_info_dict
