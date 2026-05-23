from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter


def create_pdf(report_text, filename):

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "AI Research Report",
        styles["Title"]
    )

    content.append(title)

    content.append(
        Spacer(1, 20)
    )

    body = Paragraph(
        report_text.replace("\n", "<br/>"),
        styles["BodyText"]
    )

    content.append(body)

    doc.build(content)