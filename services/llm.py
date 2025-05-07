import asyncio
import openai
from openai import RateLimitError, APIError, OpenAIError
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# Max retries and delay between retries
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

async def generate_study_plan(topic: str) -> list:
    for _ in range(MAX_RETRIES):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user",
                           "content": f"Составь подробный учебный план по теме: {topic}"}]
            )
            text = response.choices[0].message.content
            return text.strip().split("\n")
        except RateLimitError:
            await asyncio.sleep(RETRY_DELAY)
        except (APIError, OpenAIError) as e:
            return [f"Ошибка API: {str(e)}"]
    return ["Ошибка: превышен лимит запросов. Попробуйте позже."]
