import logging
from llama_cpp import Llama
from config import (
    LOCAL_LLM_MODEL_PATH,
    LOCAL_LLM_CONTEXT,
    LOCAL_LLM_THREADS,
    LOCAL_LLM_MAX_TOKENS,
)

# Configure logging
logger = logging.getLogger(__name__)


def _normalize_max_tokens(max_tokens: int) -> int:
    """Ensure max_tokens is a safe positive integer for local inference."""
    try:
        parsed = int(max_tokens)
        if parsed < 1:
            return LOCAL_LLM_MAX_TOKENS
        return min(parsed, LOCAL_LLM_CONTEXT)
    except (TypeError, ValueError):
        return LOCAL_LLM_MAX_TOKENS


# Load model once at startup
try:
    LLM_MODEL = Llama(
        model_path=LOCAL_LLM_MODEL_PATH,
        n_ctx=LOCAL_LLM_CONTEXT,
        n_threads=LOCAL_LLM_THREADS,
        verbose=False,
    )
    logger.info(
        "Local LLM model loaded successfully from: %s (ctx=%s, threads=%s)",
        LOCAL_LLM_MODEL_PATH,
        LOCAL_LLM_CONTEXT,
        LOCAL_LLM_THREADS,
    )
except Exception as e:
    logger.error("Failed to load Local LLM model from %s: %s", LOCAL_LLM_MODEL_PATH, e)
    LLM_MODEL = None


# pylint: disable=too-many-return-statements
def ask_local_llm(prompt: str, max_tokens: int = LOCAL_LLM_MAX_TOKENS) -> str:
    """Ask local LLM (offline fallback)."""
    if LLM_MODEL is None:
        return "[Local LLM error: Model not loaded]"

    if prompt is None or str(prompt).strip() == "":
        return "[Local LLM error: Empty prompt]"

    safe_max_tokens = _normalize_max_tokens(max_tokens)

    try:
        formatted_prompt = (
            "You are an educational planning assistant. "
            "Provide a concise, practical response.\n\n"
            f"User request:\n{prompt}\n\nAssistant response:\n"
        )

        output = LLM_MODEL(
            formatted_prompt,
            max_tokens=safe_max_tokens,
            temperature=0.7,
            top_p=0.9,
            stop=["\n\nUser request:", "<end_of_turn>"],
        )

        choices = output.get("choices", []) if isinstance(output, dict) else []
        if choices:
            response = str(choices[0].get("text", "")).strip()
            if response:
                logger.info("Local LLM generated response successfully")
                return response
            logger.warning("Local LLM returned empty response")
            return "[Local LLM error: Empty response]"

        logger.warning("Local LLM returned invalid output format")
        return "[Local LLM error: Invalid output format]"

    except Exception as e:
        logger.error("Local LLM error: %s", e)
        return f"[Local LLM error: {str(e)}]"
