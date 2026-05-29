import argparse

try:
    from .content_pipeline import (
        build_content_generation_prompt,
        build_idea_generation_prompt,
        generate_content,
        generate_post_ideas,
    )
    from .document_processor import DocumentProcessingError
    from .knowledge_base import load_knowledge_base
    from .llm_integration import LLMIntegrationError
    from .output_saver import OutputSaveError, save_markdown_output
    from .prompt_templates import PromptTemplateError
except ImportError:
    from content_pipeline import (
        build_content_generation_prompt,
        build_idea_generation_prompt,
        generate_content,
        generate_post_ideas,
    )
    from document_processor import DocumentProcessingError
    from knowledge_base import load_knowledge_base
    from llm_integration import LLMIntegrationError
    from output_saver import OutputSaveError, save_markdown_output
    from prompt_templates import PromptTemplateError


PREVIEW_LENGTH = 500


def build_preview(text: str, max_length: int = PREVIEW_LENGTH) -> str:
    """Return a compact preview that is readable in the terminal."""
    compact_text = " ".join(text.split())
    if len(compact_text) <= max_length:
        return compact_text
    return f"{compact_text[:max_length].rstrip()}..."


def print_file_names(title: str, file_names: list[str]) -> None:
    print(f"\n{title}")
    for file_name in file_names:
        print(f"  - {file_name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check the knowledge base and optionally generate post ideas."
    )
    parser.add_argument(
        "--generate-ideas",
        action="store_true",
        help="Call the OpenAI API to generate 5 LinkedIn post ideas.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "carousel", "listicle"],
        help="Content format to build or generate.",
    )
    parser.add_argument(
        "--idea",
        help="Selected content idea to use for format-specific content generation.",
    )
    parser.add_argument(
        "--generate-content",
        action="store_true",
        help="Call the OpenAI API to generate content for --idea and --format.",
    )
    parser.add_argument(
        "--save-output",
        action="store_true",
        help="Save generated ideas or content as markdown in outputs/.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("Personal Brand Content Creator - Knowledge Base Check")
    print("-" * 55)

    try:
        knowledge_base = load_knowledge_base()
    except DocumentProcessingError as error:
        print(f"Error: {error}")
        raise SystemExit(1) from error

    primary_file_names = [
        document.file_name for document in knowledge_base.primary_documents
    ]
    secondary_file_names = [
        document.file_name for document in knowledge_base.secondary_documents
    ]

    print(f"Primary files loaded: {len(primary_file_names)}")
    print(f"Secondary files loaded: {len(secondary_file_names)}")

    print_file_names("Primary file names:", primary_file_names)
    print_file_names("Secondary file names:", secondary_file_names)

    print("\nCombined context preview:")
    print(build_preview(knowledge_base.combined_context))

    try:
        idea_prompt = build_idea_generation_prompt(knowledge_base)
    except PromptTemplateError as error:
        print(f"\nPrompt template error: {error}")
        raise SystemExit(1) from error

    print("\nIdea generation prompt preview:")
    print(build_preview(idea_prompt))

    if args.format or args.idea or args.generate_content:
        if not args.format or not args.idea:
            print("\nContent prompt skipped. Provide both --format and --idea.")
            raise SystemExit(1)

        try:
            content_prompt = build_content_generation_prompt(
                knowledge_base=knowledge_base,
                selected_idea=args.idea,
                content_format=args.format,
            )
        except (PromptTemplateError, ValueError) as error:
            print(f"\nContent prompt error: {error}")
            raise SystemExit(1) from error

        print(f"\n{args.format.title()} content prompt preview:")
        print(build_preview(content_prompt))

        if args.generate_content:
            try:
                content = generate_content(
                    knowledge_base=knowledge_base,
                    selected_idea=args.idea,
                    content_format=args.format,
                )
            except LLMIntegrationError as error:
                print(f"\nContent generation error: {error}")
                raise SystemExit(1) from error

            print(f"\nGenerated {args.format} content:")
            print(content)

            if args.save_output:
                try:
                    file_path = save_markdown_output(
                        content=content,
                        output_type=args.format,
                        selected_idea=args.idea,
                    )
                except OutputSaveError as error:
                    print(f"\nOutput save error: {error}")
                    raise SystemExit(1) from error
                print(f"\nSaved output: {file_path}")
            return

        print("\nContent generation skipped. Add --generate-content to call OpenAI.")

    if not args.generate_ideas:
        if not args.format and not args.idea and not args.generate_content:
            print("\nIdea generation skipped. Run with --generate-ideas to call OpenAI.")
        return

    try:
        ideas = generate_post_ideas(knowledge_base)
    except LLMIntegrationError as error:
        print(f"\nIdea generation error: {error}")
        raise SystemExit(1) from error

    print("\nGenerated LinkedIn post ideas:")
    print(ideas)

    if args.save_output:
        try:
            file_path = save_markdown_output(
                content=ideas,
                output_type="ideas",
            )
        except OutputSaveError as error:
            print(f"\nOutput save error: {error}")
            raise SystemExit(1) from error
        print(f"\nSaved output: {file_path}")


if __name__ == "__main__":
    main()
