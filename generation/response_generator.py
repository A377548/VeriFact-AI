
from generation.llm_client import GeminiClient, MODEL_NAME


class ResponseGenerator:
    """
    Generates the original answer for a given user question.
    """

    def __init__(self):
        # Initialize the Gemini client
        self.gemini = GeminiClient()

    def generate_original_response(self, question: str) -> dict:
        """
        Generate an original answer and return structured information.
        """

        # Validate the question
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        # Generate the answer using Gemini
        answer = self.gemini.generate_text(question.strip())

        # Return structured output
        return {
            "question": question.strip(),
            "answer": answer,
            "model": MODEL_NAME
        }
