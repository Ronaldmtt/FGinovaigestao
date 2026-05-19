"""Configuração central do provedor de IA.

O projeto usa o SDK `openai` porque a API da DeepSeek é compatível com o
formato OpenAI. A partir daqui, todas as chamadas de chat devem sair pela
DeepSeek por padrão.
"""
import os

import httpx
from openai import OpenAI

AI_PROVIDER = "deepseek"
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")


def get_ai_model(default: str | None = None) -> str:
    """Retorna o modelo padrão de chat para a DeepSeek."""
    return os.environ.get("AI_MODEL") or DEEPSEEK_MODEL or default or "deepseek-chat"


def get_ai_api_key() -> str:
    """Retorna a chave ativa da DeepSeek."""
    return DEEPSEEK_API_KEY


def has_ai_api_key() -> bool:
    return bool(get_ai_api_key())


def missing_ai_key_message() -> str:
    return "DEEPSEEK_API_KEY não configurada no .env"


def get_ai_client(timeout: float = 120.0, max_retries: int = 0) -> OpenAI:
    """Cria cliente compatível com OpenAI apontando para DeepSeek por padrão."""
    kwargs = {
        "api_key": get_ai_api_key(),
        "timeout": timeout,
        "max_retries": max_retries,
        "http_client": httpx.Client(timeout=timeout),
    }
    kwargs["base_url"] = DEEPSEEK_BASE_URL
    return OpenAI(**kwargs)
