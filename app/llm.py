"""Fábrica única de modelos. Troque de fornecedor mudando LLM_MODEL no .env."""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama

load_dotenv()

def get_llm(model: str | None = None, temperature: float = 0.0, **kwargs):
    """Retorna o modelo de linguagem especificado no .env ou passado como argumento."""
    model = model or os.environ["LLM_MODEL"]
    return init_chat_model(model, temperature=temperature, **kwargs)

def get_llm_local(model: str | None = None, temperature: float = 0.0, **kwargs):
    """Retorna o modelo de linguagem local especificado no .env ou passado como argumento."""
    model = model or os.environ["LLM_MODEL_LOCAL"]
    base_url = os.environ["OLLAMA_BASE_URL"]
    return ChatOllama(model=model, base_url=base_url, temperature=temperature, **kwargs)
