from dataclasses import dataclass


@dataclass
class LLMConfigParams:
    DEFAULT_MODEL: str = "qwen2.5:14b-instruct-q4_K_M"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    MIROSTAT: int = 0


# Create a singleton instance
config = LLMConfigParams()
