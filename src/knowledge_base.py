from dataclasses import dataclass
from pathlib import Path

try:
    from .document_processor import (
        MarkdownDocument,
        documents_to_context,
        load_markdown_documents,
    )
except ImportError:
    from document_processor import (
        MarkdownDocument,
        documents_to_context,
        load_markdown_documents,
    )


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRIMARY_KNOWLEDGE_BASE = PROJECT_ROOT / "knowledge_base" / "primary"
SECONDARY_KNOWLEDGE_BASE = PROJECT_ROOT / "knowledge_base" / "secondary"


@dataclass(frozen=True)
class KnowledgeBase:
    primary_documents: list[MarkdownDocument]
    secondary_documents: list[MarkdownDocument]

    @property
    def primary_context(self) -> str:
        return documents_to_context(self.primary_documents)

    @property
    def secondary_context(self) -> str:
        return documents_to_context(self.secondary_documents)

    @property
    def combined_context(self) -> str:
        return "\n\n".join([self.primary_context, self.secondary_context])


def load_knowledge_base(
    primary_folder: Path = PRIMARY_KNOWLEDGE_BASE,
    secondary_folder: Path = SECONDARY_KNOWLEDGE_BASE,
) -> KnowledgeBase:
    """Load primary and secondary markdown knowledge bases separately."""
    return KnowledgeBase(
        primary_documents=load_markdown_documents(primary_folder, "primary"),
        secondary_documents=load_markdown_documents(secondary_folder, "secondary"),
    )


def get_knowledge_contexts(
    primary_folder: Path = PRIMARY_KNOWLEDGE_BASE,
    secondary_folder: Path = SECONDARY_KNOWLEDGE_BASE,
) -> tuple[str, str]:
    """Return primary context and secondary context as separate strings."""
    knowledge_base = load_knowledge_base(primary_folder, secondary_folder)
    return knowledge_base.primary_context, knowledge_base.secondary_context
