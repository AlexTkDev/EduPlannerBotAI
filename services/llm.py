import logging
import asyncio
from openai import OpenAI, RateLimitError, APIError, OpenAIError
from config import OPENAI_API_KEY

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
        "Review the learned material regularly"
    ]

    return plan


async def generate_study_plan(topic: str) -> list:
    """Generate a study plan using OpenAI API or fallback to local generation"""
    # Check if OpenAI API key is set and client is initialized
    if not OPENAI_API_KEY or client is None:
        logger.warning("OpenAI API key is missing or OpenAI client is not initialized, using local generator")
        return generate_local_plan(topic)

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(
                "Generating study plan for topic: %s (attempt %s/%s)",
                topic, attempt + 1, MAX_RETRIES)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user",
                           "content": f"Create a detailed study plan for the topic: {topic}. "
                                      f"Split the plan into 5-7 steps."}]
            )

            text = response.choices[0].message.content
            if not text:
                logger.error("OpenAI response content is None, falling back to local plan")
                return generate_local_plan(topic)
            return text.strip().split("\n")

        except RateLimitError as e:
            # Calculate exponential backoff delay
            exponential_delay = BASE_RETRY_DELAY * (2 ** attempt)
            logger.warning("Rate limit error: %s. Retrying in %s seconds...",
                           str(e), exponential_delay)
            await asyncio.sleep(exponential_delay)

        except (APIError, OpenAIError) as e:
            logger.error("OpenAI API error: %s", str(e))
            logger.info("Falling back to local plan generator")
            return generate_local_plan(topic)

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Unexpected error: %s", str(e))
            return generate_local_plan(topic)

    # If all attempts fail, fallback to local generator
    logger.warning("All OpenAI API attempts failed, using local generator")
    return generate_local_plan(topic)
