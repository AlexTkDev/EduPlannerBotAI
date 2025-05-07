import os
from fpdf import FPDF

def save_plan_to_pdf(plan_lines: list[str], user_id: int) -> str:
    os.makedirs("plans", exist_ok=True)
    filename = f"plans/plan_{user_id}.pdf"

    pdf = FPDF()
    pdf.add_page()

    # Добавляем шрифт, который поддерживает кириллицу
    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    # Добавляем текст из плана
    for line in plan_lines:
        pdf.multi_cell(0, 10, txt=line)

    pdf.output(filename)
    return filename
