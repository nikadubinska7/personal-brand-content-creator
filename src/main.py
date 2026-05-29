from pathlib import Path
from dotenv import load_dotenv
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRIMARY_KB = PROJECT_ROOT / "knowledge_base" / "primary"
SECONDARY_KB = PROJECT_ROOT / "knowledge_base" / "secondary"

def list_markdown_files(folder: Path) -> list[Path]:
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    return sorted(folder.glob("*.md"))

def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    print("Personal Brand Content Creator — Setup Test")
    print("-" * 50)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Model: {model}")
    print(f"API key loaded: {'Yes' if api_key and api_key != 'your_api_key_here' else 'No / placeholder only'}")

    primary_files = list_markdown_files(PRIMARY_KB)
    secondary_files = list_markdown_files(SECONDARY_KB)

    print(f"\nPrimary KB files found: {len(primary_files)}")
    for file in primary_files:
        print(f"  - {file.name}")

    print(f"\nSecondary KB files found: {len(secondary_files)}")
    for file in secondary_files:
        print(f"  - {file.name}")

    if len(primary_files) == 5 and len(secondary_files) == 4:
        print("\nSetup test passed.")
    else:
        print("\nSetup test warning: expected 5 primary files and 4 secondary files.")

if __name__ == "__main__":
    main()