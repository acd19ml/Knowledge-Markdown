import logging
import os
import time

from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    OpenAI,
    RateLimitError,
)


DEFAULT_TIMEOUT = float(os.environ.get("OPENAI_TIMEOUT", "120"))
DEFAULT_MAX_TOKENS = int(os.environ.get("AWM_MAX_TOKENS", "128000"))
DEFAULT_RETRY_ATTEMPTS = int(os.environ.get("AWM_API_RETRY_ATTEMPTS", "3"))
DEFAULT_RETRY_DELAY = float(os.environ.get("AWM_API_RETRY_DELAY", "5"))

logger = logging.getLogger(__name__)

RETRYABLE_EXCEPTIONS = (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
)


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


def create_chat_completion_with_retry(
    client: OpenAI,
    *,
    retry_attempts: int = DEFAULT_RETRY_ATTEMPTS,
    retry_delay: float = DEFAULT_RETRY_DELAY,
    **kwargs,
):
    """Create a chat completion with bounded retries for transient failures."""

    for attempt in range(retry_attempts + 1):
        try:
            return client.chat.completions.create(**kwargs)
        except RETRYABLE_EXCEPTIONS as exc:
            if attempt >= retry_attempts:
                raise
            wait_seconds = retry_delay * (2**attempt)
            logger.warning(
                "Chat completion failed with %s (%s/%s). Retrying in %.1fs.",
                type(exc).__name__,
                attempt + 1,
                retry_attempts + 1,
                wait_seconds,
            )
            time.sleep(wait_seconds)
