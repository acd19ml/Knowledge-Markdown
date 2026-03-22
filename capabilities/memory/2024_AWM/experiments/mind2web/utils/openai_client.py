import os

from openai import OpenAI


DEFAULT_TIMEOUT = float(os.environ.get("OPENAI_TIMEOUT", "120"))
DEFAULT_MAX_TOKENS = int(os.environ.get("AWM_MAX_TOKENS", "128000"))


def get_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("API_KEY")
    if not api_key:
        raise KeyError("Set OPENAI_API_KEY or API_KEY before running Mind2Web scripts.")
    return api_key


def get_base_url() -> str | None:
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        return base_url

    host_url = os.environ.get("HOST_URL")
    if host_url:
        return f"{host_url.rstrip('/')}/v1"

    return None


def build_openai_client() -> OpenAI:
    kwargs = {
        "api_key": get_api_key(),
        "timeout": DEFAULT_TIMEOUT,
    }
    base_url = get_base_url()
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)
