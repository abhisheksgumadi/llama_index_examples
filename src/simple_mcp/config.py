from dataclasses import dataclass

@dataclass
class LLMConfigParams:
    DEFAULT_MODEL: str = "qwen2.5:14b-instruct-q4_K_M"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    MIROSTAT: int = 0
    IS_FUNCTION_CALLING_MODEL: bool = True
    MCP_SERVER_URL: str = "http://127.0.0.1:8000/sse"

# Create a singleton instance
config = LLMConfigParams() 