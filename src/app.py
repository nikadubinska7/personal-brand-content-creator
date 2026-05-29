import streamlit as st

try:
    from .content_pipeline import (
        build_content_generation_prompt,
        build_uniqueness_comparison_prompt,
        generate_content,
        generate_post_ideas,
        generate_uniqueness_comparison,
    )
    from .document_processor import DocumentProcessingError
    from .knowledge_base import KnowledgeBase, load_knowledge_base
    from .llm_integration import LLMIntegrationError
    from .output_saver import OutputSaveError, save_markdown_output
    from .pdf_generator import PDFGenerationError, save_pdf_output
    from .prompt_templates import PromptTemplateError
except ImportError:
    from content_pipeline import (
        build_content_generation_prompt,
        build_uniqueness_comparison_prompt,
        generate_content,
        generate_post_ideas,
        generate_uniqueness_comparison,
    )
    from document_processor import DocumentProcessingError
    from knowledge_base import KnowledgeBase, load_knowledge_base
    from llm_integration import LLMIntegrationError
    from output_saver import OutputSaveError, save_markdown_output
    from pdf_generator import PDFGenerationError, save_pdf_output
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
    if "saved_output_path" not in st.session_state:
        st.session_state.saved_output_path = ""
    if "saved_pdf_path" not in st.session_state:
        st.session_state.saved_pdf_path = ""
    if "generic_output" not in st.session_state:
        st.session_state.generic_output = ""
    if "uniqueness_comparison" not in st.session_state:
        st.session_state.uniqueness_comparison = ""

    if st.button("Generate 5 Ideas", type="primary"):
        try:
            st.session_state.generated_ideas = generate_post_ideas(knowledge_base)
            st.session_state.saved_output_path = ""
            st.session_state.saved_pdf_path = ""
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
            st.session_state.saved_output_path = ""
            st.session_state.saved_pdf_path = ""

    st.subheader("3. Copy-Ready Output")
    st.text_area(
        "Generated content",
        height=360,
        placeholder="Generated content will appear here.",
        key="generated_content",
    )

    col_save_md, col_save_pdf = st.columns(2)
    with col_save_md:
        save_output_clicked = st.button("Save Markdown")
    with col_save_pdf:
        save_pdf_clicked = st.button("Save PDF")

    if save_output_clicked:
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

    if save_pdf_clicked:
        try:
            pdf_path = save_pdf_output(
                content=st.session_state.generated_content,
                output_type=content_format,
                selected_idea=selected_idea,
            )
        except PDFGenerationError as error:
            st.error(str(error))
        else:
            st.session_state.saved_pdf_path = str(pdf_path)

    if st.session_state.saved_pdf_path:
        st.success(f"Saved PDF: {st.session_state.saved_pdf_path}")

    st.divider()
    st.subheader("4. Uniqueness Evidence")
    st.text_area(
        "Generic output",
        height=180,
        placeholder="Paste a generic ChatGPT-style output here.",
        key="generic_output",
    )

    col_preview_unique, col_generate_unique = st.columns(2)
    with col_preview_unique:
        preview_uniqueness_clicked = st.button("Preview Comparison Prompt")
    with col_generate_unique:
        generate_uniqueness_clicked = st.button("Generate Comparison")

    if preview_uniqueness_clicked:
        try:
            comparison_prompt = build_uniqueness_comparison_prompt(
                knowledge_base=knowledge_base,
                generic_output=st.session_state.generic_output,
                app_output=st.session_state.generated_content,
            )
        except (PromptTemplateError, ValueError) as error:
            st.error(str(error))
        else:
            st.text_area("Comparison prompt preview", value=comparison_prompt, height=280)

    if generate_uniqueness_clicked:
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
        "Uniqueness comparison",
        height=260,
        placeholder="Comparison evidence will appear here.",
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


if __name__ == "__main__":
    main()
