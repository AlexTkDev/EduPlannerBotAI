import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


async def generate_study_plan(topic: str) -> list:
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Составь подробный учебный план по теме: {topic}"}]
    )
    text = response.choices[0].message.content
    return text.strip().split("\n")
