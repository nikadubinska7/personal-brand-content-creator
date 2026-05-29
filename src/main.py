try:
    from .document_processor import DocumentProcessingError
    from .knowledge_base import load_knowledge_base
except ImportError:
    from document_processor import DocumentProcessingError
    from knowledge_base import load_knowledge_base


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


def main() -> None:
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


if __name__ == "__main__":
    main()
