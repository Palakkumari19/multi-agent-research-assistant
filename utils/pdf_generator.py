
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter


def create_pdf(report, filename):

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    story = []

    lines = report.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # HEADINGS

        if line.startswith("# "):

            style = styles["Heading1"]

            text = line.replace("# ", "")

        elif line.startswith("## "):

            style = styles["Heading2"]

            text = line.replace("## ", "")

        elif line.startswith("### "):

            style = styles["Heading3"]

            text = line.replace("### ", "")

        else:

            style = styles["BodyText"]

            text = line

        story.append(
            Paragraph(text, style)
        )

        story.append(
            Spacer(1, 12)
        )

    doc.build(story)