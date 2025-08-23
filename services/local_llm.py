import logging
from llama_cpp import Llama

# Configure logging
logger = logging.getLogger(__name__)

# Load model once at startup
try:
    LLM_MODEL = Llama(
        model_path="models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        n_ctx=2048,  # Context window
        n_threads=4,  # Number of CPU threads
        verbose=False  # Reduce output noise
    )
    logger.info("Local LLM model loaded successfully")
except Exception as e:
    logger.error("Failed to load Local LLM model: %s", e)
    LLM_MODEL = None

def ask_local_llm(prompt: str, max_tokens: int = 512) -> str:
    """Ask local LLM (offline fallback)"""
    if LLM_MODEL is None:
        return "[Local LLM error: Model not loaded]"

    try:
        # Format prompt for better results
        formatted_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

        output = LLM_MODEL(
            formatted_prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            stop=["<|im_end|>", "\n\n"]
        )

        if output and "choices" in output and len(output["choices"]) > 0:
            response = output["choices"][0]["text"].strip()
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
