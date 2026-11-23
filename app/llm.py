"""Fábrica única de modelos. Troque de fornecedor mudando LLM_MODEL no .env."""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

def get_llm(model: str | None = None, base_url: str | None = None, temperature: float = 0.0, **kwargs):
    """Retorna o modelo de linguagem especificado no .env ou passado como argumento."""
    model = model or os.environ["LLM_MODEL"]
    if model.startswith("ollama:"):
        base_url = base_url or os.environ["OLLAMA_BASE_URL"]
    
    return init_chat_model(model, base_url=base_url, temperature=temperature, **kwargs)

