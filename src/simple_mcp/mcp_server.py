from fastmcp import FastMCP
import asyncio
import json
mcp = FastMCP('simple-mcp-server', port=8000)

@mcp.tool()
async def calculator_tool(a: int, b: int) -> int:
    """Adds two integers and returns their sum.
    
    Args:
        a (int): First integer to add
        b (int): Second integer to add
        
    Returns:
        int: The sum of a and b
    """
    return a + b

if __name__ == "__main__":
    mcp.run(transport="sse", port=8000)