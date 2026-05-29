from pathlib import Path
from re import Match, findall, sub
from typing import Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = PROJECT_ROOT / "templates"
PLACEHOLDER_PATTERN = r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}"


class PromptTemplateError(Exception):
    """Raised when prompt templates cannot be loaded or rendered clearly."""


def load_prompt_template(
    template_name: str,
    template_dir: Path = TEMPLATE_DIR,
) -> str:
    """Load a markdown prompt template by file name."""
    if Path(template_name).name != template_name:
        raise PromptTemplateError(
            f"Template name must be a file name, not a path: {template_name}"
        )

    if not template_dir.exists():
        raise PromptTemplateError(f"Prompt template folder not found: {template_dir}")

    if not template_dir.is_dir():
        raise PromptTemplateError(f"Prompt template path is not a folder: {template_dir}")

    file_name = template_name if template_name.endswith(".md") else f"{template_name}.md"
    template_path = template_dir / file_name

    if not template_path.exists():
        raise PromptTemplateError(f"Prompt template not found: {template_path}")

    template = template_path.read_text(encoding="utf-8")
    if not template.strip():
        raise PromptTemplateError(f"Prompt template is empty: {template_path}")

    return template


def render_prompt_template(
    template: str,
    values: Mapping[str, str],
) -> str:
    """Render a template with {{ placeholder }} values."""
    placeholders = set(findall(PLACEHOLDER_PATTERN, template))
    missing_values = sorted(
        placeholder for placeholder in placeholders if placeholder not in values
    )

    if missing_values:
        missing = ", ".join(missing_values)
        raise PromptTemplateError(f"Missing prompt template values: {missing}")

    def replace_placeholder(match: Match[str]) -> str:
        key = match.group(1)
        return values[key]

    return sub(PLACEHOLDER_PATTERN, replace_placeholder, template)
