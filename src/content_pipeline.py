from re import finditer, split
from typing import Literal

try:
    from .knowledge_base import KnowledgeBase
    from .llm_integration import generate_text
    from .prompt_templates import load_prompt_template, render_prompt_template
except ImportError:
    from knowledge_base import KnowledgeBase
    from llm_integration import generate_text
    from prompt_templates import load_prompt_template, render_prompt_template


IDEA_GENERATION_TEMPLATE = "idea_generation_prompt.md"
UNIQUENESS_COMPARISON_TEMPLATE = "uniqueness_comparison_prompt.md"
ContentFormat = Literal["text", "carousel", "listicle"]

CONTENT_TEMPLATES: dict[ContentFormat, str] = {
    "text": "text_post_prompt.md",
    "carousel": "carousel_prompt.md",
    "listicle": "listicle_prompt.md",
}

VISUAL_MARKERS = ("→", "•", "✅", "⚠️", "📌", "🔍", "💡", "📊", "🚚", "⏱️", "📦")
SECTION_MARKERS = {
    "the problem:": "⚠️",
    "problem:": "⚠️",
    "why it matters:": "📊",
    "where ai could help:": "💡",
    "what ai can do:": "💡",
    "what i am exploring:": "🔍",
    "example:": "📌",
    "takeaway:": "✅",
    "practical takeaway:": "✅",
    "what this made me think:": "💡",
}


def build_idea_generation_prompt(knowledge_base: KnowledgeBase) -> str:
    """Build the prompt used to generate LinkedIn content ideas."""
    template = load_prompt_template(IDEA_GENERATION_TEMPLATE)
    return render_prompt_template(
        template,
        {
            "primary_context": knowledge_base.primary_context,
            "secondary_context": knowledge_base.secondary_context,
        },
    )


def generate_post_ideas(knowledge_base: KnowledgeBase) -> str:
    """Generate 5 LinkedIn post ideas from the loaded knowledge base."""
    prompt = build_idea_generation_prompt(knowledge_base)
    return generate_text(prompt)


def parse_generated_ideas(generated_ideas: str, limit: int = 5) -> list[str]:
    """Split generated idea text into selectable idea blocks."""
    cleaned_ideas = generated_ideas.strip()
    if not cleaned_ideas:
        return []

    idea_heading_pattern = r"(?im)^\s*(?:#{1,4}\s*)?(?:(?:Post\s+)?Idea\s*\d+|\d+[\.\)])\s*[:\.\)-]?\s+.*$"
    heading_matches = list(finditer(idea_heading_pattern, cleaned_ideas))

    if heading_matches:
        blocks = []
        for index, match in enumerate(heading_matches):
            start = match.start()
            end = (
                heading_matches[index + 1].start()
                if index + 1 < len(heading_matches)
                else len(cleaned_ideas)
            )
            block = cleaned_ideas[start:end].strip(" \n-")
            if block and idea_label(block):
                blocks.append(block)
        return blocks[:limit]

    blocks = [
        block.strip(" \n-")
        for block in split(r"\n\s*\n", cleaned_ideas)
        if block.strip()
    ]

    return [block for block in blocks if idea_label(block)][:limit]


def idea_label(idea: str, max_length: int = 140) -> str:
    """Return a clean one-line label for a generated idea block."""
    for line in idea.splitlines():
        compact_line = " ".join(line.strip(" -").split())
        if compact_line:
            return (
                compact_line
                if len(compact_line) <= max_length
                else f"{compact_line[: max_length - 3].rstrip()}..."
            )
    return ""


def build_content_generation_prompt(
    knowledge_base: KnowledgeBase,
    selected_idea: str,
    content_format: ContentFormat,
) -> str:
    """Build a format-specific content generation prompt."""
    if not selected_idea.strip():
        raise ValueError("A selected idea is required to build a content prompt.")

    template = load_prompt_template(CONTENT_TEMPLATES[content_format])
    return render_prompt_template(
        template,
        {
            "selected_idea": selected_idea.strip(),
            "primary_context": knowledge_base.primary_context,
            "secondary_context": knowledge_base.secondary_context,
        },
    )


def count_visual_markers(content: str) -> int:
    """Count visible structure markers in generated content."""
    return sum(content.count(marker) for marker in VISUAL_MARKERS)


def add_section_marker(line: str) -> str:
    """Add a relevant marker to a known section label when missing."""
    stripped_line = line.strip()
    if stripped_line.startswith(VISUAL_MARKERS):
        return line

    lower_line = stripped_line.lower()
    for section_label, marker in SECTION_MARKERS.items():
        if lower_line.startswith(section_label):
            indentation = line[: len(line) - len(line.lstrip())]
            return f"{indentation}{marker} {stripped_line}"

    return line


def format_linkedin_post_output(content: str, content_format: ContentFormat) -> str:
    """Lightly add scan-friendly symbols when the model returns plain text."""
    if not content.strip():
        return content

    formatted_lines: list[str] = []
    bullet_markers_added = 0
    for line in [add_section_marker(line) for line in content.strip().splitlines()]:
        stripped_line = line.lstrip()
        indentation = line[: len(line) - len(stripped_line)]

        if stripped_line.startswith(("- ", "* ")):
            bullet_body = stripped_line[2:].strip()
            if bullet_body.lower().startswith(("takeaway:", "practical takeaway:")):
                formatted_lines.append(f"{indentation}✅ {bullet_body}")
                bullet_markers_added += 1
                continue

            if bullet_markers_added < 4:
                formatted_lines.append(f"{indentation}→ {bullet_body}")
                bullet_markers_added += 1
                continue

        if content_format == "listicle" and stripped_line.startswith("→ "):
            bullet_markers_added += 1

        formatted_lines.append(line)

    formatted_content = "\n".join(formatted_lines).strip()
    if count_visual_markers(formatted_content) >= 4:
        return formatted_content

    if content_format == "text":
        return f"🔍 {formatted_content}"
    if content_format == "carousel":
        if "Caption:\n" in formatted_content:
            return formatted_content.replace("Caption:\n", "Caption:\n🔍 ", 1)
        if "Caption:" in formatted_content:
            return formatted_content.replace("Caption:", "Caption:\n🔍", 1)
        return f"🔍 {formatted_content}"

    if "Caption:\n" in formatted_content:
        return formatted_content.replace("Caption:\n", "Caption:\n📌 ", 1)
    if "Caption:" in formatted_content:
        return formatted_content.replace("Caption:", "Caption:\n📌", 1)
    return f"📌 {formatted_content}"


def generate_content(
    knowledge_base: KnowledgeBase,
    selected_idea: str,
    content_format: ContentFormat,
) -> str:
    """Generate LinkedIn content for the selected format."""
    prompt = build_content_generation_prompt(
        knowledge_base=knowledge_base,
        selected_idea=selected_idea,
        content_format=content_format,
    )
    return format_linkedin_post_output(generate_text(prompt), content_format)


def build_uniqueness_comparison_prompt(
    knowledge_base: KnowledgeBase,
    generic_output: str,
    app_output: str,
) -> str:
    """Build a prompt that compares generic output with app-generated output."""
    if not generic_output.strip():
        raise ValueError("Generic output is required for uniqueness comparison.")
    if not app_output.strip():
        raise ValueError("App output is required for uniqueness comparison.")

    template = load_prompt_template(UNIQUENESS_COMPARISON_TEMPLATE)
    return render_prompt_template(
        template,
        {
            "primary_context": knowledge_base.primary_context,
            "secondary_context": knowledge_base.secondary_context,
            "generic_output": generic_output.strip(),
            "app_output": app_output.strip(),
        },
    )


def generate_uniqueness_comparison(
    knowledge_base: KnowledgeBase,
    generic_output: str,
    app_output: str,
) -> str:
    """Generate written uniqueness evidence for project documentation."""
    prompt = build_uniqueness_comparison_prompt(
        knowledge_base=knowledge_base,
        generic_output=generic_output,
        app_output=app_output,
    )
    return generate_text(prompt)
