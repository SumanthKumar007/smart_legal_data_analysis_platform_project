import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from logger import logger

def generate_report(user_queries, ai_responses):
    # Ensure the folder exists
    folder_name = "chat_reports"
    os.makedirs(folder_name, exist_ok=True)

    # Create a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"AI_Lawyer_Report_{timestamp}.pdf"
    pdf_path = os.path.join(folder_name, pdf_filename)

    # Create the PDF
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "AI Lawyer Report")
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, "Below is a record of your conversation with AI Lawyer.")

    y = 700
    for q, a in zip(user_queries, ai_responses):
        q_lines = simpleSplit(f"Q: {q}", "Helvetica-Bold", 12, 450)
        a_lines = simpleSplit(f"A: {a}", "Helvetica", 12, 450)
        for line in q_lines + a_lines:
            c.drawString(100, y, line)
            y -= 15
            if y < 50:
                c.showPage()
                y = 750

    c.save()

    # Log the creation of the report
    logger.info(f"Chat report generated as PDF: {pdf_path}")
    return pdf_path
