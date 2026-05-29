import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


DEFAULT_MODEL = "gpt-4o-mini"


class LLMIntegrationError(Exception):
    """Raised when the LLM request cannot be completed clearly."""


def get_model_name() -> str:
    """Read the model name from the environment with a small local default."""
    load_dotenv()
    return os.getenv("LLM_MODEL", DEFAULT_MODEL)


def get_openai_client() -> OpenAI:
    """Create an OpenAI client using OPENAI_API_KEY from the environment."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your_api_key_here":
        raise LLMIntegrationError(
            "OPENAI_API_KEY is missing. Add it to .env before generating ideas."
        )

    return OpenAI(api_key=api_key)


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
