import logging
import asyncio
from openai import OpenAI, RateLimitError, APIError, OpenAIError
from config import OPENAI_API_KEY

# Настройка логгера
logger = logging.getLogger(__name__)

# Initialize client
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Max retries and delay between retries
MAX_RETRIES = 3
RETRY_DELAY = 5  # Увеличиваем задержку между попытками


# Локальный генератор
def generate_local_plan(topic: str) -> list:
    """Generate a basic study plan without using API"""
    logger.info("Using local plan generator for topic: %s", topic)

    plan = [
        f"Учебный план по теме: {topic}",
        "",
        "Шаг 1. Изучите основы темы",
        f"Шаг 2. Ознакомьтесь с ключевыми концепциями {topic}",
        f"Шаг 3. Исследуйте примеры использования {topic}",
        "Шаг 4. Выполните практические задания",
        "Шаг 5. Закрепите материал с помощью упражнений",
        "Шаг 6. Создайте собственный проект",
        "",
        "Регулярно повторяйте изученный материал"
    ]

    return plan


async def generate_study_plan(topic: str) -> list:
    """Generate a study plan using OpenAI API or fallback to local generation"""
    # Проверка наличия API ключа
    if not OPENAI_API_KEY:
        logger.warning("OpenAI API key is missing, using local generator")
        return generate_local_plan(topic)

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(
                "Generating study plan for topic: %s (attempt %s/%s)",
                topic, attempt + 1, MAX_RETRIES)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user",
                           "content": f"Составь подробный учебный план по теме: {topic}. "
                                      f"Раздели план на 5-7 шагов."}]
            )

            text = response.choices[0].message.content
            return text.strip().split("\n")

        except RateLimitError as e:
            logger.warning("Rate limit error: %s. Retrying in %s seconds...",
                           str(e), RETRY_DELAY * (attempt + 1))
            await asyncio.sleep(RETRY_DELAY * (attempt + 1))  # Экспоненциальная задержка

        except (APIError, OpenAIError) as e:
            logger.error("OpenAI API error: %s", str(e))
            logger.info("Falling back to local plan generator")
            return generate_local_plan(topic)

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Unexpected error: %s", str(e))
            return generate_local_plan(topic)

    # Если все попытки исчерпаны, используем локальный генератор
    logger.warning("All OpenAI API attempts failed, using local generator")
    return generate_local_plan(topic)
