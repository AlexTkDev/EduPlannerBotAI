import logging
import asyncio
import httpx  # third party import should be first
from openai import OpenAI, RateLimitError, APIError, OpenAIError
from config import OPENAI_API_KEY
from config import GROQ_API_KEY
from .local_llm import ask_local_llm


# Configure logging
logger = logging.getLogger(__name__)

# Initialize client
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Max retries and delay between retries
MAX_RETRIES = 3
BASE_RETRY_DELAY = 5  # Base delay in seconds

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


# pylint: disable=too-many-return-statements
async def generate_study_plan(topic: str) -> list:
    """Generate study plan with fallback chain: OpenAI → Groq → Local LLM → Simple Plan"""

    # Try OpenAI first
    if OPENAI_API_KEY and client is not None:
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(
                    "Generating study plan for topic: %s (attempt %s/%s)",
                    topic, attempt + 1, MAX_RETRIES)

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": (
                                f"Create a detailed study plan for the topic: {topic}. "
                                f"Split the plan into 5-7 steps."
                            ),
                        }
                    ],
                )

                text = response.choices[0].message.content
                if not text:
                    logger.error("OpenAI response content is None, falling back to Groq")
                    break
                return text.strip().split("\n")

            except RateLimitError as e:
                exponential_delay = BASE_RETRY_DELAY * (2 ** attempt)
                logger.warning("Rate limit error: %s. Retrying in %s seconds...",
                               str(e), exponential_delay)
                await asyncio.sleep(exponential_delay)

            except (APIError, OpenAIError) as e:
                logger.error("OpenAI API error: %s", str(e))
                logger.info("Falling back to Groq generator")
                break

            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error("Unexpected error: %s", str(e))
                logger.info("Falling back to Groq generator")
                break

    # Try Groq as fallback
    if GROQ_API_KEY:
        try:
            logger.info("OpenAI failed, trying Groq for topic: %s", topic)
            return await generate_groq_plan(topic)
        except Exception as e:
            logger.error("Groq fallback error: %s", e)
            logger.info("Falling back to Local LLM")

    # Try Local LLM as fallback
    try:
        logger.info("Groq failed, trying Local LLM for topic: %s", topic)
        text = ask_local_llm(
            f"Create a detailed study plan for the topic: {topic}. "
            f"Split the plan into 5-7 steps."
        )
        if text and not text.startswith("[Local LLM error:"):
            return text.split("\n")
        logger.warning("Local LLM returned error, falling back to simple plan")
    except Exception as e:
        logger.error("Local LLM error: %s", e)
        logger.info("Falling back to simple plan")

    # Final fallback: simple local plan
    logger.info("All LLM services failed, using simple local plan for topic: %s", topic)
    return generate_local_plan(topic)

async def translate_text(text: str, target_lang: str) -> str:
    """Translate text with fallback chain: OpenAI → Groq → Local LLM → Original text"""
    if target_lang == 'en':
        return text

    prompt = (
        f"Translate the following text to {target_lang}. "
        f"Output only the translation, no explanations, no extra text.\n{text}"
    )
    logger.info("Translating to %s: %s", target_lang, text)

    # Try OpenAI first
    if OPENAI_API_KEY and client is not None:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            translated = response.choices[0].message.content
            logger.info("OpenAI translation result: %s", translated)
            if translated:
                return translated.strip()
        except Exception:  # pylint: disable=broad-exception-caught
            logger.warning("OpenAI translation failed, trying Groq")

    # Try Groq as fallback
    if GROQ_API_KEY:
        try:
            logger.info("OpenAI failed, trying Groq for translation to %s", target_lang)
            return await groq_translate_text(text, target_lang)
        except Exception as e:
            logger.error("Groq translation fallback error: %s", e)
            logger.info("Falling back to Local LLM")

    # Try Local LLM as fallback
    try:
        logger.info("Groq failed, trying Local LLM for translation to %s", target_lang)
        translated = ask_local_llm(
            f"Translate the following text to {target_lang}. "
            f"Output only the translation:\n{text}"
        )
        if translated and not translated.startswith("[Local LLM error:"):
            return translated.strip()
        logger.warning("Local LLM translation returned error, keeping original text")
    except Exception as e:
        logger.error("Local LLM translation error: %s", e)
        logger.info("Keeping original text as final fallback")

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
        "model": "llama3-8b-8192",
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
            return ["[Groq error: unable to generate plan]"]
        except Exception as e:
            logger.error(f"Groq unexpected error: {e}")
            return ["[Groq error: unable to generate plan]"]

async def groq_translate_text(text: str, target_lang: str) -> str:
    if target_lang == 'en':
        return text
    if not GROQ_API_KEY:
        return text
    prompt = (
        f"Translate the following text to {target_lang}. "
        f"Output only the translation, no explanations, no extra text.\n{text}"
    )
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            translated = response.json()["choices"][0]["message"]["content"]
            if translated:
                return translated.strip()
        except Exception as e:
            logger.error(f"Groq translation error: {e}")
    return text
