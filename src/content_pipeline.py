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
ContentFormat = Literal["text", "carousel", "listicle"]

CONTENT_TEMPLATES: dict[ContentFormat, str] = {
    "text": "text_post_prompt.md",
    "carousel": "carousel_prompt.md",
    "listicle": "listicle_prompt.md",
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
    return generate_text(prompt)
