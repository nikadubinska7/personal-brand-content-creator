from datetime import datetime
from html import escape
from pathlib import Path
from re import match

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

try:
    from .output_saver import OUTPUT_DIR, slugify
except ImportError:
    from output_saver import OUTPUT_DIR, slugify


PDF_FORMATS = {"carousel", "listicle"}


class PDFGenerationError(Exception):
    """Raised when PDF export cannot be completed clearly."""


def clean_markdown_line(line: str) -> str:
    """Convert lightweight markdown markers into readable paragraph text."""
    stripped = line.strip()
    for marker in ("### ", "## ", "# "):
        if stripped.startswith(marker):
            return stripped.removeprefix(marker).strip()
    if stripped.startswith("- "):
        return f"- {stripped.removeprefix('- ').strip()}"
    return stripped


def split_content_sections(content: str) -> list[list[str]]:
    """Split generated content into readable PDF sections."""
    sections: list[list[str]] = []
    current_section: list[str] = []

    for line in content.splitlines():
        cleaned_line = clean_markdown_line(line)
        if not cleaned_line:
            continue

        starts_new_section = (
            cleaned_line.lower().startswith("slide ")
            or match(r"^\d+[\.\)]\s+", cleaned_line) is not None
        )

        if starts_new_section and current_section:
            sections.append(current_section)
            current_section = []

        current_section.append(cleaned_line)

    if current_section:
        sections.append(current_section)

    return sections or [[content.strip()]]


def save_pdf_output(
    content: str,
    output_type: str,
    selected_idea: str | None = None,
    output_dir: Path = OUTPUT_DIR,
) -> Path:
    """Save generated carousel or listicle content as a readable PDF."""
    if output_type not in PDF_FORMATS:
        raise PDFGenerationError(
            "PDF export is currently supported for carousel and listicle content."
        )

    if not content.strip():
        raise PDFGenerationError("Generated output is empty and was not exported.")

    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    idea_slug = slugify(selected_idea or output_type, fallback=output_type)
    output_slug = slugify(output_type)
    file_path = output_dir / f"{timestamp}-{output_slug}-{idea_slug}.pdf"

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "PDFTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=28,
        spaceAfter=18,
    )
    heading_style = ParagraphStyle(
        "PDFHeading",
        parent=styles["Heading2"],
        fontSize=16,
        leading=21,
        spaceAfter=10,
    )
    body_style = ParagraphStyle(
        "PDFBody",
        parent=styles["BodyText"],
        fontSize=11,
        leading=15,
        spaceAfter=8,
    )

    document = SimpleDocTemplate(
        str(file_path),
        pagesize=letter,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )

    story = [
        Paragraph(f"{output_type.title()} Content", title_style),
    ]
    if selected_idea:
        story.append(Paragraph(f"Idea: {escape(selected_idea.strip())}", body_style))
    story.append(Spacer(1, 0.2 * inch))

    sections = split_content_sections(content)
    for section_index, section in enumerate(sections):
        if section_index:
            story.append(PageBreak())

        heading = section[0]
        story.append(Paragraph(escape(heading), heading_style))

        for line in section[1:]:
            story.append(Paragraph(escape(line), body_style))

    document.build(story)
    return file_path
