from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter


def create_pdf(content, filename):

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    story = []

    paragraphs = content.split("\n")

    for para in paragraphs:

        if para.strip():

            p = Paragraph(
                para,
                styles["BodyText"]
            )

            story.append(p)

            story.append(
                Spacer(1, 12)
            )

    doc.build(story)