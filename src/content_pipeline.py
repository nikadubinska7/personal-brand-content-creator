try:
    from .knowledge_base import KnowledgeBase
    from .llm_integration import generate_text
    from .prompt_templates import load_prompt_template, render_prompt_template
except ImportError:
    from knowledge_base import KnowledgeBase
    from llm_integration import generate_text
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


def generate_post_ideas(knowledge_base: KnowledgeBase) -> str:
    """Generate 5 LinkedIn post ideas from the loaded knowledge base."""
    prompt = build_idea_generation_prompt(knowledge_base)
    return generate_text(prompt)
