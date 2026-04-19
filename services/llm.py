import logging
import asyncio
import os
from concurrent.futures import ProcessPoolExecutor
import httpx  # third party import should be first
from openai import OpenAI
from config import OPENAI_API_KEY
from config import GROQ_API_KEY
from config import OPENAI_MODEL
from config import GROQ_MODEL
from services.local_llm import ask_local_llm


# Configure logging
logger = logging.getLogger(__name__)

# Initialize client
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Max retries and delay between retries
MAX_RETRIES = 3
BASE_RETRY_DELAY = 5  # Base delay in seconds

# Optional multiprocessing for local LLM
USE_PROCESS_LLM = str(os.getenv("USE_PROCESS_LLM", "0")).lower() not in ("0", "false", "no", "")
PROCESS_EXECUTOR = ProcessPoolExecutor(max_workers=(os.cpu_count() or 2)) if USE_PROCESS_LLM else None

async def _ask_local_llm_async(prompt: str, max_tokens: int = 512) -> str:
    """Run local LLM either in a separate process (if enabled) or a thread."""
    if USE_PROCESS_LLM and PROCESS_EXECUTOR is not None:
        loop = asyncio.get_running_loop()
        # Pass only prompt, rely on default max_tokens in ask_local_llm, or pass explicitly
        return await loop.run_in_executor(PROCESS_EXECUTOR, ask_local_llm, prompt, max_tokens)
    # Threaded fallback to preserve test monkeypatching and responsiveness
    return await asyncio.to_thread(ask_local_llm, prompt, max_tokens)

async def _race_first_success(tasks):
    """Race given coroutine tasks and return the first non-empty/valid result.
    Cancels remaining tasks after first success.
    """
    pending = {asyncio.create_task(coro) for coro in tasks if coro is not None}
    try:
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for d in done:
                try:
                    result = d.result()
                    # Valid results: non-empty string or non-empty list
                    if isinstance(result, list) and result:
                        return result
                    if isinstance(result, str) and result.strip() != "":
                        return result
                except Exception:  # pylint: disable=broad-exception-caught
                    # Ignore failed task and continue
                    continue
        return None
    finally:
        for p in pending:
            p.cancel()

async def _openai_plan_async(topic: str):
    if not (OPENAI_API_KEY and client is not None):
        return None
    def _call():
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": (
                f"Create a detailed study plan for the topic: {topic}. "
                f"Split the plan into 5-7 steps." )}],
        )
        return response.choices[0].message.content if response and response.choices else None
    try:
        text = await asyncio.to_thread(_call)
        return text.strip().split("\n") if text else None
    except Exception:  # pylint: disable=broad-exception-caught
        return None

async def _openai_translate_async(prompt: str):
    if not (OPENAI_API_KEY and client is not None):
        return None
    def _call():
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content if response and response.choices else None
    try:
        text = await asyncio.to_thread(_call)
        return text.strip() if text else None
    except Exception:  # pylint: disable=broad-exception-caught
        return None

# Local plan generator
def generate_local_plan(topic: str) -> list:
    """Generate a basic study plan without using the API"""
    logger.info("Using local plan generator for topic: %s", topic)

    plan = [
        f"📚 Study Plan for: {topic}",
        "",
        "🎯 Step 1: Foundation",
        f"   • Research basic concepts of {topic}",
        "   • Understand the core principles",
        "   • Identify key terminology",
        "",
        "📖 Step 2: Deep Dive",
        f"   • Study advanced concepts of {topic}",
        "   • Read relevant documentation",
        "   • Watch tutorial videos",
        "",
        "💻 Step 3: Practical Application",
        "   • Complete hands-on exercises",
        "   • Work on small projects",
        "   • Practice with real examples",
        "",
        "🔍 Step 4: Problem Solving",
        "   • Solve practice problems",
        "   • Work through case studies",
        "   • Identify common challenges",
        "",
        "📝 Step 5: Review & Reinforcement",
        "   • Summarize key learnings",
        "   • Create study notes",
        "   • Test your knowledge",
        "",
        "🚀 Step 6: Advanced Topics",
        "   • Explore advanced features",
        "   • Learn best practices",
        "   • Stay updated with latest trends",
        "",
        "💡 Tips for Success:",
        "   • Study consistently, even if just 30 minutes daily",
        "   • Practice regularly to reinforce learning",
        "   • Join study groups or online communities",
        "   • Don't hesitate to ask questions",
        "",
        "📅 Recommended Study Schedule:",
        "   • Week 1-2: Steps 1-2 (Foundation & Deep Dive)",
        "   • Week 3-4: Steps 3-4 (Practical & Problem Solving)",
        "   • Week 5-6: Steps 5-6 (Review & Advanced Topics)",
        "",
        "Good luck with your studies! 🎉"
    ]

    return plan


# pylint: disable=too-many-return-statements, too-many-branches
async def generate_study_plan(topic: str) -> list:
    """Generate study plan with aggressive concurrency: race OpenAI and Groq;
    fallback to Local LLM (threaded/process) → Simple Plan.
    """

    # If both OpenAI and Groq available, race them
    if (OPENAI_API_KEY and client is not None) and GROQ_API_KEY:
        logger.info("Racing OpenAI and Groq for topic: %s", topic)
        result = await _race_first_success([
            _openai_plan_async(topic),
            generate_groq_plan(topic),
        ])
        if isinstance(result, list) and result:
            return result
        logger.info("Race returned no valid result, falling back")

    # If only OpenAI available, try it with retries (threaded)
    if OPENAI_API_KEY and client is not None:
        for attempt in range(MAX_RETRIES):
            try:
                logger.info("OpenAI-only plan generation attempt %s/%s for %s",
                            attempt + 1, MAX_RETRIES, topic)
                lines = await _openai_plan_async(topic)
                if lines:
                    return lines
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error("OpenAI plan attempt failed: %s", e)
            exponential_delay = BASE_RETRY_DELAY * (2 ** attempt)
            await asyncio.sleep(exponential_delay)

    # If only Groq available, try it
    if GROQ_API_KEY:
        try:
            logger.info("Using Groq for topic: %s", topic)
            lines = await generate_groq_plan(topic)
            if lines:
                return lines
        except Exception as e:
            logger.error("Groq error: %s", e)

    # Try Local LLM as fallback (threaded/process based on settings)
    try:
        logger.info("Trying Local LLM for topic: %s", topic)
        prompt = (
            f"Create a detailed study plan for the topic: {topic}. "
            f"Split the plan into 5-7 steps."
        )
        text = await _ask_local_llm_async(prompt)
        if text and not text.startswith("[Local LLM error:"):
            lines = text.split("\n")
            if any(topic in line for line in lines):
                return lines
            logger.warning("Local LLM returned plan without topic mention, falling back to simple plan")
        else:
            logger.warning("Local LLM returned error, falling back to simple plan")
    except Exception as e:
        logger.error("Local LLM error: %s", e)

    # Final fallback: simple local plan
    logger.info("All LLM services failed, using simple local plan for topic: %s", topic)
    return generate_local_plan(topic)

# pylint: disable=too-many-branches
async def translate_text(text: str, target_lang: str) -> str:
    """Translate text with aggressive concurrency: race OpenAI and Groq; fallback to
    Local LLM (threaded) → Original text.
    """
    # Handle empty or whitespace-only text
    if text is None or str(text).strip() == "":
        return text

    # Normalize language code (e.g., 'ru-RU' -> 'ru', 'es_ES' -> 'es')
    lang = (target_lang or "en").strip().lower()
    if "-" in lang:
        lang = lang.split("-")[0]
    if "_" in lang:
        lang = lang.split("_")[0]

    if lang == 'en':
        return text

    prompt = (
        f"Translate the following text to {lang}. "
        f"Output only the translation, no explanations, no extra text.\n{text}"
    )
    logger.info("Translating to %s: %s", lang, text)

    # If both providers available, race them
    if (OPENAI_API_KEY and client is not None) and GROQ_API_KEY:
        logger.info("Racing OpenAI and Groq for translation to %s", lang)
        winner = await _race_first_success([
            _openai_translate_async(prompt),
            groq_translate_text(text, lang),
        ])
        if isinstance(winner, str) and winner.strip() != "":
            return winner.strip()

    # If only OpenAI available
    if OPENAI_API_KEY and client is not None:
        try:
            translated = await _openai_translate_async(prompt)
            if translated:
                return translated.strip()
        except Exception:  # pylint: disable=broad-exception-caught
            logger.warning("OpenAI translation failed, trying next fallback")

    # If only Groq available
    if GROQ_API_KEY:
        try:
            translated = await groq_translate_text(text, lang)
            if translated:
                return translated.strip()
        except Exception as e:
            logger.error("Groq translation error: %s", e)

    # Local LLM fallback (process/thread based on settings)
    try:
        logger.info("Trying Local LLM for translation to %s", lang)
        prompt_local = (
            f"Translate the following text to {lang}. "
            f"Output only the translation:\n{text}"
        )
        translated = await _ask_local_llm_async(prompt_local)
        if translated and not translated.startswith("[Local LLM error:"):
            return translated.strip()
        logger.warning("Local LLM translation returned error, keeping original text")
    except Exception as e:
        logger.error("Local LLM translation error: %s", e)

    # Final fallback: return original text
    return text

async def generate_groq_plan(topic: str) -> list:
    if not GROQ_API_KEY:
        raise RuntimeError("Groq API key not set")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Create a detailed study plan for the topic: {topic}. "
                    f"Split the plan into 5-7 steps."
                ),
            }
        ],
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            text = response.json()["choices"][0]["message"]["content"]
            return text.strip().split("\n")
        except httpx.HTTPStatusError as e:
            logger.error(f"Groq HTTP error: {e}")
            # Raise to allow upper-level fallback (Local LLM -> Simple plan)
            raise RuntimeError("Groq error: unable to generate plan") from e
        except Exception as e:
            logger.error(f"Groq unexpected error: {e}")
            # Raise to allow upper-level fallback
            raise RuntimeError("Groq error: unable to generate plan") from e

async def groq_translate_text(text: str, target_lang: str) -> str | None:
    # Handle empty text early
    if text is None or str(text).strip() == "":
        return text
    # Normalize lang (defensive, though translate_text already normalizes)
    lang = (target_lang or "en").strip().lower()
    if "-" in lang:
        lang = lang.split("-")[0]
    if "_" in lang:
        lang = lang.split("_")[0]
    if lang == 'en':
        return text
    if not GROQ_API_KEY:
        return None
    prompt = (
        f"Translate the following text to {lang}. "
        f"Output only the translation, no explanations, no extra text.\n{text}"
    )
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            translated = response.json()["choices"][0]["message"]["content"]
            if translated:
                return translated.strip()
            return None
        except Exception as e:
            logger.error(f"Groq translation error: {e}")
            return None
