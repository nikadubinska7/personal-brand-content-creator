from datetime import datetime
from pathlib import Path
from re import sub


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "outputs"
POST_OUTPUT_DIR = OUTPUT_DIR / "posts"
PDF_OUTPUT_DIR = OUTPUT_DIR / "pdfs"
IMAGE_OUTPUT_DIR = OUTPUT_DIR / "images"


class OutputSaveError(Exception):
    """Raised when generated output cannot be saved clearly."""


def slugify(value: str, fallback: str = "output") -> str:
    """Create a readable filename segment from user-facing text."""
    slug = sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug[:60] or fallback


def front_matter_value(value: str) -> str:
    """Format a value safely for simple YAML front matter."""
    clean_value = " ".join(value.split()).replace('"', '\\"')
    return f'"{clean_value}"'


def save_markdown_output(
    content: str,
    output_type: str,
    selected_idea: str | None = None,
    output_dir: Path = POST_OUTPUT_DIR,
) -> Path:
    """Save generated content as a markdown file in the posts output folder."""
    if not content.strip():
        raise OutputSaveError("Generated output is empty and was not saved.")

    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    idea_slug = slugify(selected_idea or output_type, fallback=output_type)
    output_slug = slugify(output_type)
    file_path = output_dir / f"{timestamp}-{output_slug}-{idea_slug}.md"

    metadata = [
        "---",
        f"output_type: {front_matter_value(output_type)}",
        f"created_at: {front_matter_value(datetime.now().isoformat(timespec='seconds'))}",
    ]
    if selected_idea:
        metadata.append(f"selected_idea: {front_matter_value(selected_idea)}")
    metadata.extend(["---", ""])

    file_path.write_text(
        "\n".join(metadata) + content.strip() + "\n",
        encoding="utf-8",
    )

    return file_path
