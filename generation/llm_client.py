
import os

from dotenv import load_dotenv
from google import genai


# Load environment variables from the .env file
load_dotenv()

# Gemini model used by VeriFact AI
MODEL_NAME = "gemini-3.8-flash"


class GeminiClient:
    """
    Handles communication between VeriFact AI and Gemini.
    """

    def __init__(self):
        # Read the API key from environment variables
        api_key = os.getenv("GEMINI_API_KEY")

        # Stop if the API key is missing
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Check your .env file."
            )

        # Create the Gemini API client
        self.client = genai.Client(api_key=api_key)

    def generate_text(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return its text response.
        """

        # Validate the prompt
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            # Send the request to Gemini
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

        except Exception as exc:
            error_message = str(exc)

            if "503" in error_message or "UNAVAILABLE" in error_message:
              raise RuntimeError(
            "Gemini is temporarily unavailable due to high demand. "
            "Please try again after some time."
             ) from exc

            raise RuntimeError(
               f"Gemini API request failed: {exc}"
           ) from exc

        # Extract generated text
        generated_text = response.text

        # Check whether Gemini returned a valid response
        if not generated_text or not generated_text.strip():
            raise RuntimeError("Gemini returned an empty response.")

        return generated_text.strip()
