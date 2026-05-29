import streamlit as st

try:
    from .content_pipeline import (
        build_content_generation_prompt,
        build_uniqueness_comparison_prompt,
        generate_content,
        generate_post_ideas,
        generate_uniqueness_comparison,
        parse_generated_ideas,
    )
    from .document_processor import DocumentProcessingError
    from .knowledge_base import KnowledgeBase, load_knowledge_base
    from .llm_integration import LLMIntegrationError
    from .output_saver import OutputSaveError, save_markdown_output
    from .prompt_templates import PromptTemplateError
except ImportError:
    from content_pipeline import (
        build_content_generation_prompt,
        build_uniqueness_comparison_prompt,
        generate_content,
        generate_post_ideas,
        generate_uniqueness_comparison,
        parse_generated_ideas,
    )
    from document_processor import DocumentProcessingError
    from knowledge_base import KnowledgeBase, load_knowledge_base
    from llm_integration import LLMIntegrationError
    from output_saver import OutputSaveError, save_markdown_output
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


def format_idea_label(idea: str) -> str:
    first_line = next(
        (line.strip() for line in idea.splitlines() if line.strip()),
        idea,
    )
    compact_idea = " ".join(first_line.split())
    if len(compact_idea) <= 140:
        return compact_idea
    return f"{compact_idea[:137].rstrip()}..."


@st.dialog("Uniqueness Evidence")
def show_uniqueness_dialog(knowledge_base: KnowledgeBase) -> None:
    st.caption("Compare a generic baseline with the current app-generated output.")
    st.text_area(
        "Generic output",
        height=180,
        placeholder="Paste a generic ChatGPT-style output here.",
        key="generic_output",
    )

    if st.button("Preview Comparison Prompt"):
        try:
            comparison_prompt = build_uniqueness_comparison_prompt(
                knowledge_base=knowledge_base,
                generic_output=st.session_state.generic_output,
                app_output=st.session_state.generated_content,
            )
        except (PromptTemplateError, ValueError) as error:
            st.error(str(error))
        else:
            st.text_area("Comparison prompt preview", value=comparison_prompt, height=260)

    if st.button("Generate Comparison", type="primary"):
        try:
            comparison = generate_uniqueness_comparison(
                knowledge_base=knowledge_base,
                generic_output=st.session_state.generic_output,
                app_output=st.session_state.generated_content,
            )
        except (LLMIntegrationError, PromptTemplateError, ValueError) as error:
            st.error(str(error))
        else:
            st.session_state.uniqueness_comparison = comparison

    st.text_area(
        "Structured comparison",
        height=260,
        placeholder="Comparison table will appear here.",
        key="uniqueness_comparison",
    )

    if st.button("Save Comparison"):
        try:
            file_path = save_markdown_output(
                content=st.session_state.uniqueness_comparison,
                output_type="uniqueness-comparison",
            )
        except OutputSaveError as error:
            st.error(str(error))
        else:
            st.success(f"Saved comparison: {file_path}")


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

    if "generated_ideas" not in st.session_state:
        st.session_state.generated_ideas = ""
    if "selected_idea" not in st.session_state:
        st.session_state.selected_idea = ""
    if "generated_content" not in st.session_state:
        st.session_state.generated_content = ""
    if "saved_output_path" not in st.session_state:
        st.session_state.saved_output_path = ""
    if "generic_output" not in st.session_state:
        st.session_state.generic_output = ""
    if "uniqueness_comparison" not in st.session_state:
        st.session_state.uniqueness_comparison = ""

    with st.expander("Knowledge base files", expanded=False):
        show_loaded_files(knowledge_base)

    left_column, right_column = st.columns([0.42, 0.58], gap="large")

    with left_column:
        st.subheader("Create")

        if st.button("Generate 5 Ideas", type="primary", use_container_width=True):
            try:
                st.session_state.generated_ideas = generate_post_ideas(knowledge_base)
                st.session_state.selected_idea = ""
                st.session_state.saved_output_path = ""
            except LLMIntegrationError as error:
                st.error(str(error))

        ideas = parse_generated_ideas(st.session_state.generated_ideas)
        if ideas:
            selected_idea = st.radio(
                "Select an idea",
                options=ideas,
                format_func=format_idea_label,
                key="selected_idea_choice",
            )
            st.session_state.selected_idea = selected_idea
        else:
            selected_idea = ""
            st.info("Generate ideas to choose one for content creation.")

        content_format = st.radio(
            "Choose format",
            options=["text", "carousel", "listicle"],
            horizontal=True,
        )

        preview_clicked = st.button("Preview Prompt", use_container_width=True)
        generate_clicked = st.button(
            "Generate Post",
            type="primary",
            use_container_width=True,
        )

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
                st.text_area("Prompt preview", value=prompt, height=260)

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
                st.session_state.saved_output_path = ""

        st.divider()
        if st.button("Save Markdown", use_container_width=True):
            try:
                file_path = save_markdown_output(
                    content=st.session_state.generated_content,
                    output_type=content_format,
                    selected_idea=selected_idea,
                )
            except OutputSaveError as error:
                st.error(str(error))
            else:
                st.session_state.saved_output_path = str(file_path)

        if st.session_state.saved_output_path:
            st.success(f"Saved output: {st.session_state.saved_output_path}")

        if st.button("Open Uniqueness Evidence", use_container_width=True):
            show_uniqueness_dialog(knowledge_base)

    with right_column:
        st.subheader("Generated Post")
        st.text_area(
            "LinkedIn-ready output",
            height=720,
            placeholder="Generated content will appear here.",
            key="generated_content",
            label_visibility="collapsed",
        )


if __name__ == "__main__":
    main()
