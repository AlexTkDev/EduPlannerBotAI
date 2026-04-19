import os
from dotenv import load_dotenv

load_dotenv()


def _get_int_env(var_name: str, default: int, min_value: int = 1) -> int:
    """Parse integer env var safely with fallback to default.

    Invalid or out-of-range values are ignored to keep startup stable.
    """
    raw_value = os.getenv(var_name)
    if raw_value is None:
        return default
    try:
        parsed_value = int(raw_value)
        if parsed_value < min_value:
            return default
        return parsed_value
    except (TypeError, ValueError):
        return default


TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

LOCAL_LLM_MODEL_PATH = os.getenv("LOCAL_LLM_MODEL_PATH", "models/google-gemma-4b-it-Q4_K_M.gguf")
LOCAL_LLM_CONTEXT = _get_int_env("LOCAL_LLM_CONTEXT", default=4096, min_value=512)
LOCAL_LLM_THREADS = _get_int_env("LOCAL_LLM_THREADS", default=4, min_value=1)
LOCAL_LLM_MAX_TOKENS = _get_int_env("LOCAL_LLM_MAX_TOKENS", default=512, min_value=32)
