from dataclasses import dataclass


@dataclass
class LLMConfigParams:
    DEFAULT_MODEL: str = "qwen2.5:14b-instruct-q4_K_M"


# Create a singleton instance
config = LLMConfigParams()
