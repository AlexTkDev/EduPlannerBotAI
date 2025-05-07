import os
from fpdf import FPDF


def save_plan_to_pdf(plan_lines: list[str], user_id: int) -> str:
    # Create directories if they don't exist
    os.makedirs("plans", exist_ok=True)
    os.makedirs("fonts", exist_ok=True)

    filename = f"plans/plan_{user_id}.pdf"

    # Создаем простой PDF без кастомных шрифтов, которые могут отсутствовать
    pdf = FPDF()
    pdf.add_page()

    # Use standard font if DejaVu is not available
    try:
        # Check if font file exists
        if os.path.exists("fonts/DejaVuSans.ttf"):
            pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
            pdf.set_font("DejaVu", size=12)
        else:
            # Fallback to standard font
            pdf.set_font("Arial", size=12)
    except Exception:
        # If error with custom font, use standard
        pdf.set_font("Arial", size=12)

    # Convert non-Latin characters to ensure compatibility
    for line in plan_lines:
        try:
            pdf.multi_cell(0, 10, txt=line)
        except Exception:
            # Handle encoding issues
            pdf.multi_cell(0, 10, txt="[Text encoding error]")

    pdf.output(filename)
    return filename
