from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings
from .config import config


class LLMConfig:
    def __init__(self, model_name: str = config.DEFAULT_MODEL):
        self.llm = Ollama(model=model_name)
        Settings.llm = self.llm
        Settings.embed_model = OllamaEmbedding(
            model_name=model_name,
            base_url=config.OLLAMA_BASE_URL,
            ollama_additional_kwargs={"mirostat": config.MIROSTAT},
        )
