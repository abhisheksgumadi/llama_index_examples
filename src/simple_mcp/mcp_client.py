import asyncio
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import ReActAgent, FunctionAgent
from llama_index.llms.ollama import Ollama
from llama_index.tools.mcp import (
    get_tools_from_mcp_url,
    aget_tools_from_mcp_url,
)
from llama_index.core.settings import Settings
from config import config


async def main():
    # Connect to your MCP server
    mcp_client = BasicMCPClient(config.MCP_SERVER_URL)
    mcp_tool_spec = McpToolSpec(client=mcp_client)

    tools = await mcp_tool_spec.to_tool_list_async()

    llm = Ollama(
        model=config.DEFAULT_MODEL,
        base_url=config.OLLAMA_BASE_URL,
        mirostat=config.MIROSTAT,
        is_function_calling_model=config.IS_FUNCTION_CALLING_MODEL,
    )
    Settings.llm = llm

    # 4. Create an agent with the MCP tools
    agent = FunctionAgent(
        tools=tools,
        system_prompt="You are an AI assistant for Tool Calling. You have access to the following tools: calculator_tool.",
    )

    # Run a query through the agent
    response = await agent.run("How much 10 + 2?")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
