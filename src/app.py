import streamlit as st

try:
    from .content_pipeline import (
        build_content_generation_prompt,
        generate_content,
        generate_post_ideas,
    )
    from .document_processor import DocumentProcessingError
    from .knowledge_base import KnowledgeBase, load_knowledge_base
    from .llm_integration import LLMIntegrationError
    from .prompt_templates import PromptTemplateError
except ImportError:
    from content_pipeline import (
        build_content_generation_prompt,
        generate_content,
        generate_post_ideas,
    )
    from document_processor import DocumentProcessingError
    from knowledge_base import KnowledgeBase, load_knowledge_base
    from llm_integration import LLMIntegrationError
    from prompt_templates import PromptTemplateError


def load_app_knowledge_base() -> KnowledgeBase:
    return load_knowledge_base()


def show_loaded_files(knowledge_base: KnowledgeBase) -> None:
    primary_names = [document.file_name for document in knowledge_base.primary_documents]
    secondary_names = [
        document.file_name for document in knowledge_base.secondary_documents
    ]

    col_primary, col_secondary = st.columns(2)
    with col_primary:
        st.metric("Primary files", len(primary_names))
        st.write(primary_names)

    with col_secondary:
        st.metric("Secondary files", len(secondary_names))
        st.write(secondary_names)


def main() -> None:
    st.set_page_config(
        page_title="Personal Brand Content Creator",
        layout="wide",
    )

    st.title("Personal Brand Content Creator")
    st.caption("Local MVP for LinkedIn content based on markdown knowledge files.")

    try:
        knowledge_base = load_app_knowledge_base()
    except DocumentProcessingError as error:
        st.error(str(error))
        st.stop()

    show_loaded_files(knowledge_base)

    st.divider()

    st.subheader("1. Generate Or Paste An Idea")
    if "generated_ideas" not in st.session_state:
        st.session_state.generated_ideas = ""
    if "selected_idea" not in st.session_state:
        st.session_state.selected_idea = ""
    if "generated_content" not in st.session_state:
        st.session_state.generated_content = ""

    if st.button("Generate 5 Ideas", type="primary"):
        try:
            st.session_state.generated_ideas = generate_post_ideas(knowledge_base)
        except LLMIntegrationError as error:
            st.error(str(error))

    st.text_area(
        "Generated ideas",
        height=220,
        key="generated_ideas",
    )

    selected_idea = st.text_area(
        "Selected idea",
        height=120,
        placeholder="Paste one idea here before generating content.",
        key="selected_idea",
    )

    st.subheader("2. Choose Format")
    content_format = st.selectbox(
        "Content format",
        options=["text", "carousel", "listicle"],
    )

    col_preview, col_generate = st.columns(2)
    with col_preview:
        preview_clicked = st.button("Preview Prompt")
    with col_generate:
        generate_clicked = st.button("Generate Content", type="primary")

    if preview_clicked:
        try:
            prompt = build_content_generation_prompt(
                knowledge_base=knowledge_base,
                selected_idea=selected_idea,
                content_format=content_format,
            )
        except (PromptTemplateError, ValueError) as error:
            st.error(str(error))
        else:
            st.text_area("Prompt preview", value=prompt, height=320)

    if generate_clicked:
        try:
            content = generate_content(
                knowledge_base=knowledge_base,
                selected_idea=selected_idea,
                content_format=content_format,
            )
        except (LLMIntegrationError, PromptTemplateError, ValueError) as error:
            st.error(str(error))
        else:
            st.session_state.generated_content = content

    st.subheader("3. Copy-Ready Output")
    st.text_area(
        "Generated content",
        height=360,
        placeholder="Generated content will appear here.",
        key="generated_content",
    )


if __name__ == "__main__":
    main()
