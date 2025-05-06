from fpdf import FPDF


def save_plan_to_pdf(plan: list, user_id: int) -> str:
    filename = f"plan_{user_id}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in plan:
        pdf.multi_cell(0, 10, txt=line)
    pdf.output(filename)
    return filename
