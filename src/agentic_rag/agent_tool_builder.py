from typing import Callable, Dict, List
from llama_index.core.tools import FunctionTool
from llama_index.core.agent.workflow import FunctionAgent


class AgentToolBuilder:
    def __init__(self, agents_dict: Dict, extra_info_dict: Dict):
        self.agents_dict = agents_dict
        self.extra_info_dict = extra_info_dict

    def get_agent_tool_callable(self, agent: FunctionAgent) -> Callable:
        async def query_agent(query: str) -> str:
            response = await agent.run(query)
            return str(response)

        return query_agent

    def build_tools(self) -> List[FunctionTool]:
        all_tools = []
        for file_base, agent in self.agents_dict.items():
            summary = self.extra_info_dict[file_base]["summary"]
            async_fn = self.get_agent_tool_callable(agent)
            doc_tool = FunctionTool.from_defaults(
                async_fn,
                name=f"tool_{file_base}",
                description=summary,
            )
            all_tools.append(doc_tool)
        return all_tools
