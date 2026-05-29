try:
    from .knowledge_base import KnowledgeBase
    from .prompt_templates import load_prompt_template, render_prompt_template
except ImportError:
    from knowledge_base import KnowledgeBase
    from prompt_templates import load_prompt_template, render_prompt_template


IDEA_GENERATION_TEMPLATE = "idea_generation_prompt.md"


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
