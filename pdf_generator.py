from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io


def generate_pdf(text):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )

    story = []

    lines = text.split("\n")

    for line in lines:

        clean = line.strip()

        if clean == "":
            story.append(Spacer(1, 10))
            continue

        # Title
        if clean.startswith("Project Title"):
            story.append(Paragraph(clean, title_style))

        # Section headers
        elif clean.startswith("Problem Statement") or \
             clean.startswith("System Architecture") or \
             clean.startswith("Tech Stack") or \
             clean.startswith("Dataset Suggestions") or \
             clean.startswith("Estimated Timeline") or \
             clean.startswith("Development Plan"):

            story.append(Paragraph(clean, section_style))

        else:
            story.append(Paragraph(clean, body_style))

    doc.build(story)

    buffer.seek(0)

    return buffer