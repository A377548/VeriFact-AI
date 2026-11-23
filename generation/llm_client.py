
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"


class GeminiClient:
    """
    Handles communication between VeriFact AI and Gemini.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Check your .env file."
            )

        self.client = genai.Client(api_key=api_key)

    def _generate(self, prompt: str, json_mode: bool = False) -> str:

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        config = {
            "http_options": {"timeout": 30000},
            "max_output_tokens": 2048
        }

        if json_mode:
            config["response_mime_type"] = "application/json"

        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=config
            )

        except Exception as exc:
            error_message = str(exc)

            if "503" in error_message or "UNAVAILABLE" in error_message:
                raise RuntimeError(
                    "Gemini is temporarily unavailable due to high demand. "
                    "Please try again later."
                ) from exc

            raise RuntimeError(
                f"Gemini API request failed: {exc}"
            ) from exc

        generated_text = response.text

        if not generated_text or not generated_text.strip():
            raise RuntimeError("Gemini returned an empty response.")

        return generated_text.strip()

    def generate_text(self, prompt: str) -> str:
        """
        Generate ordinary natural-language text.
        """
        return self._generate(prompt, json_mode=False)

    def generate_json(self, prompt: str) -> str:
        """
        Generate JSON-formatted output.
        """
        return self._generate(prompt, json_mode=True)
