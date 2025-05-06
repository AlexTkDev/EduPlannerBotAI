from aiogram import Router, types
from services.llm import generate_study_plan
from services.pdf import save_plan_to_pdf
from services.chart import generate_study_chart
from services.reminders import schedule_reminders
from services.db import save_user_plan

router = Router()

@router.message()
async def handle_message(message: types.Message):
    query = message.text.strip()
    plan = await generate_study_plan(query)
    pdf_path = save_plan_to_pdf(plan, message.from_user.id)
    chart_path = generate_study_chart(plan, message.from_user.id)
    save_user_plan(message.from_user.id, plan)
    await schedule_reminders(message.from_user.id, plan)

    await message.answer_document(document=types.FSInputFile(pdf_path),
                                  caption="📘 Твой учебный план")
    await message.answer_photo(photo=types.FSInputFile(chart_path),
                               caption="📊 График обучения")
