# Simple MCP (Message Control Protocol) Implementation

This project demonstrates a simple implementation of the Message Control Protocol (MCP) using FastMCP and LlamaIndex. It consists of a server that exposes tools and a client that can interact with these tools using an LLM agent.

## Project Structure

```
simple_mcp/
├── config.py         # Configuration settings
├── mcp_server.py     # MCP server implementation
└── mcp_client.py     # MCP client implementation
```

## Prerequisites

- Python 3.8+
- Ollama running locally (for LLM functionality)
- Required Python packages:
  - fastmcp
  - llama-index
  - llama-index-llms-ollama

## Configuration

The `config.py` file contains the following configuration parameters:

- `DEFAULT_MODEL`: The Ollama model to use (default: "qwen2.5:14b-instruct-q4_K_M")
- `OLLAMA_BASE_URL`: URL for the Ollama service (default: "http://localhost:11434")
- `MIROSTAT`: Mirostat parameter for the LLM (default: 0)
- `IS_FUNCTION_CALLING_MODEL`: Whether the model supports function calling (default: True)
- `MCP_SERVER_URL`: URL for the MCP server (default: "http://127.0.0.1:8000/sse")

## Components

### MCP Server (`mcp_server.py`)

The server component exposes tools that can be called by the client. Currently, it implements a simple calculator tool that adds two integers.

```python
@mcp.tool()
async def calculator_tool(a: int, b: int) -> int:
    """Adds two integers and returns their sum."""
    return a + b
```

The server runs on port 8000 and uses Server-Sent Events (SSE) for communication.

### MCP Client (`mcp_client.py`)

The client component:
1. Connects to the MCP server
2. Creates an LLM agent using Ollama
3. Loads the available tools from the server
4. Processes user queries using the agent

## Running the Project

1. Start the MCP server:
   ```bash
   python mcp_server.py
   ```

2. In a separate terminal, run the client:
   ```bash
   python mcp_client.py
   ```

The client will connect to the server and process the example query "How much 10 + 2?" using the calculator tool.

## Example Usage

The client demonstrates how to:
- Connect to an MCP server
- Create an LLM agent with MCP tools
- Process natural language queries that get translated into tool calls

You can modify the query in `mcp_client.py` to test different calculations or add more tools to the server.

## Extending the Project

To add more tools:
1. Add new tool functions in `mcp_server.py` using the `@mcp.tool()` decorator
2. Update the system prompt in `mcp_client.py` to include the new tools
3. Restart both the server and client

## Notes

- Make sure Ollama is running and the specified model is available before running the client
- The server must be running before starting the client
- The current implementation uses a simple calculator tool, but you can extend it with more complex tools as needed
