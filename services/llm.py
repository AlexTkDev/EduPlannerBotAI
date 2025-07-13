import logging
import asyncio
import httpx  # third party import should be first
from openai import OpenAI, RateLimitError, APIError, OpenAIError
from config import OPENAI_API_KEY
from config import GROQ_API_KEY

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
        f"Study plan for topic: {topic}",
        "",
        "Step 1. Learn the basics of the topic",
        f"Step 2. Get familiar with key concepts of {topic}",
        f"Step 3. Explore usage examples of {topic}",
        "Step 4. Complete practical tasks",
        "Step 5. Reinforce the material with exercises",
        "Step 6. Create your own project",
        "",
        "Review the learned material regularly",
    ]

    return plan


# pylint: disable=too-many-return-statements
async def generate_study_plan(topic: str) -> list:
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
    try:
        return await generate_groq_plan(topic)
    except Exception as e:
        logger.error(f"Groq fallback error: {e}")
    # Fallback: local
    return generate_local_plan(topic)

async def translate_text(text: str, target_lang: str) -> str:
    if target_lang == 'en':
        return text
    prompt = (
        f"Translate the following text to {target_lang}. "
        f"Output only the translation, no explanations, no extra text.\n{text}"
    )
    logger.info(f"Translating to {target_lang}: {text}")
    # Try OpenAI
    if OPENAI_API_KEY and client is not None:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            translated = response.choices[0].message.content
            logger.info(f"OpenAI translation result: {translated}")
            if translated:
                return translated.strip()
        except Exception:  # pylint: disable=broad-exception-caught
            logger.warning("OpenAI translation failed, trying Groq")
    # Try Groq as fallback
    try:
        return await groq_translate_text(text, target_lang)
    except Exception as e:
        logger.error(f"Groq translation fallback error: {e}")
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
