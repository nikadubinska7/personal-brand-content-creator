from html import escape
from json import dumps

import streamlit as st
import streamlit.components.v1 as components

try:
    from .content_pipeline import (
        build_content_generation_prompt,
        build_uniqueness_comparison_prompt,
        generate_content,
        generate_post_ideas,
        generate_uniqueness_comparison,
        idea_label,
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
        idea_label,
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


def render_post_preview(content: str) -> None:
    if not content.strip():
        st.info("Generated content will appear here.")
        return

    st.markdown(content.replace("\n", "  \n"))


def render_copy_button(content: str) -> None:
    disabled = "disabled" if not content.strip() else ""
    escaped_content = dumps(content)
    components.html(
        f"""
        <button
            {disabled}
            id="copy-post-button"
            style="
                width: 140px;
                padding: 0.65rem 0.9rem;
                border: 1px solid #d0d5dd;
                border-radius: 0.45rem;
                background: #ffffff;
                color: #1f2937;
                font: 600 0.95rem system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
                cursor: pointer;
            "
        >
            Copy post
        </button>
        <span id="copy-post-status" style="margin-left: 0.75rem; color: #667085; font: 0.9rem system-ui;"></span>
        <script>
            const button = document.getElementById("copy-post-button");
            const status = document.getElementById("copy-post-status");
            button?.addEventListener("click", async () => {{
                await navigator.clipboard.writeText({escaped_content});
                status.textContent = "Copied";
                setTimeout(() => status.textContent = "", 1800);
            }});
        </script>
        """,
        height=48,
    )


def parse_markdown_table(markdown_text: str) -> list[dict[str, str]]:
    table_lines = [
        line.strip()
        for line in markdown_text.splitlines()
        if line.strip().startswith("|") and line.strip().endswith("|")
    ]
    if len(table_lines) < 3:
        return []

    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []

    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells, strict=False)))

    return rows


def render_comparison_table(rows: list[dict[str, str]]) -> None:
    if not rows:
        return

    headers = list(rows[0].keys())
    header_html = "".join(f"<th>{escape(header)}</th>" for header in headers)
    row_html = ""
    for row in rows:
        row_html += "<tr>"
        for header in headers:
            row_html += f"<td>{escape(row.get(header, ''))}</td>"
        row_html += "</tr>"

    st.markdown(
        f"""
        <style>
            .comparison-table-wrapper {{
                max-height: 520px;
                overflow: auto;
                border: 1px solid #e4e7ec;
                border-radius: 8px;
            }}
            .comparison-table {{
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed;
                font-size: 0.82rem;
                line-height: 1.35;
            }}
            .comparison-table th {{
                position: sticky;
                top: 0;
                background: #f8fafc;
                z-index: 1;
                text-align: left;
                font-weight: 700;
                color: #344054;
            }}
            .comparison-table th,
            .comparison-table td {{
                border-bottom: 1px solid #e4e7ec;
                border-right: 1px solid #e4e7ec;
                padding: 0.55rem;
                vertical-align: top;
                overflow-wrap: anywhere;
                word-break: normal;
            }}
            .comparison-table th:first-child,
            .comparison-table td:first-child {{
                width: 15%;
                font-weight: 650;
            }}
        </style>
        <div class="comparison-table-wrapper">
            <table class="comparison-table">
                <thead><tr>{header_html}</tr></thead>
                <tbody>{row_html}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.dialog("Uniqueness Evidence", width="large")
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

    comparison_rows = parse_markdown_table(st.session_state.uniqueness_comparison)
    if comparison_rows:
        render_comparison_table(comparison_rows)
    elif st.session_state.uniqueness_comparison:
        st.warning("The comparison did not include a readable table.")

    with st.expander("Raw comparison text", expanded=not comparison_rows):
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
            idea_options = list(range(len(ideas)))
            selected_idea_index = st.radio(
                "Select an idea",
                options=idea_options,
                format_func=lambda index: idea_label(ideas[index]),
                key="selected_idea_choice",
            )
            selected_idea = ideas[selected_idea_index]
            st.session_state.selected_idea = selected_idea

            with st.expander("Selected idea details", expanded=False):
                st.write(selected_idea)
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
        with st.container(border=True):
            render_post_preview(st.session_state.generated_content)

        render_copy_button(st.session_state.generated_content)


if __name__ == "__main__":
    main()
