from dataclasses import dataclass
from pathlib import Path
from typing import Literal


SourceType = Literal["primary", "secondary"]


class DocumentProcessingError(Exception):
    """Raised when markdown documents cannot be loaded clearly."""


@dataclass(frozen=True)
class MarkdownDocument:
    file_name: str
    source_type: SourceType
    content: str
    path: Path


def load_markdown_documents(
    folder: Path,
    source_type: SourceType,
) -> list[MarkdownDocument]:
    """Load all markdown files from a knowledge-base folder."""
    if not folder.exists():
        raise DocumentProcessingError(
            f"Missing {source_type} knowledge base folder: {folder}"
        )

    if not folder.is_dir():
        raise DocumentProcessingError(
            f"Expected {source_type} knowledge base path to be a folder: {folder}"
        )

    markdown_files = sorted(folder.glob("*.md"))
    if not markdown_files:
        raise DocumentProcessingError(
            f"No markdown files found in {source_type} knowledge base folder: {folder}"
        )

    documents: list[MarkdownDocument] = []
    for file_path in markdown_files:
        documents.append(
            MarkdownDocument(
                file_name=file_path.name,
                source_type=source_type,
                content=file_path.read_text(encoding="utf-8"),
                path=file_path,
            )
        )

    return documents


def documents_to_context(documents: list[MarkdownDocument]) -> str:
    """Combine documents into prompt-ready context while keeping filenames visible."""
    sections = []
    for document in documents:
        sections.append(
            f"## {document.source_type.title()} source: {document.file_name}\n\n"
            f"{document.content.strip()}"
        )

    return "\n\n".join(sections)
