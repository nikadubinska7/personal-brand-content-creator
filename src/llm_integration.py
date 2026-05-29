import os
from pathlib import Path

from dotenv import dotenv_values, load_dotenv
from openai import OpenAI, OpenAIError


DEFAULT_MODEL = "gpt-4o-mini"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"
API_KEY_PLACEHOLDER = "your_api_key_here"


class LLMIntegrationError(Exception):
    """Raised when the LLM request cannot be completed clearly."""


def load_project_env() -> None:
    """Load environment variables from the project .env file."""
    load_dotenv(dotenv_path=ENV_FILE)


def get_api_key() -> str:
    """Read OPENAI_API_KEY, falling back to .env if the shell has a placeholder."""
    load_project_env()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key and api_key != API_KEY_PLACEHOLDER:
        return api_key

    env_values = dotenv_values(ENV_FILE) if ENV_FILE.exists() else {}
    file_api_key = env_values.get("OPENAI_API_KEY")

    if file_api_key and file_api_key != API_KEY_PLACEHOLDER:
        return file_api_key

    raise LLMIntegrationError(
        f"OPENAI_API_KEY is missing. Add it to {ENV_FILE} before generating ideas."
    )


def get_model_name() -> str:
    """Read the model name from the environment with a small local default."""
    load_project_env()
    return os.getenv("LLM_MODEL", DEFAULT_MODEL)


def get_openai_client() -> OpenAI:
    """Create an OpenAI client using OPENAI_API_KEY from the environment."""
    return OpenAI(api_key=get_api_key())


def generate_text(prompt: str, model: str | None = None) -> str:
    """Generate text from a prompt using the OpenAI Responses API."""
    client = get_openai_client()
    selected_model = model or get_model_name()

    try:
        response = client.responses.create(
            model=selected_model,
            input=prompt,
        )
    except OpenAIError as error:
        raise LLMIntegrationError(f"OpenAI request failed: {error}") from error

    output_text = response.output_text.strip()
    if not output_text:
        raise LLMIntegrationError("OpenAI returned an empty response.")

    return output_text
