
from generation.llm_client import GeminiClient, MODEL_NAME


class SampleGenerator:
    """
    Generates multiple independent responses for the same question.
    These responses will later be used for consistency analysis.
    """

    def __init__(self):
        self.gemini = GeminiClient()

    def generate_samples(
        self,
        question: str,
        number_of_samples: int = 3
    ) -> dict:
        """
        Generate independent answers and preserve successful samples
        even if some API requests fail.
        """

        # Validate the question
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        # Validate the number of samples
        if (
            isinstance(number_of_samples, bool)
            or not isinstance(number_of_samples, int)
            or number_of_samples < 1
        ):
            raise ValueError(
                "Number of samples must be a positive integer."
            )

        samples = []
        errors = []

        prompt = (
            "Answer the following question directly and independently. "
            "Provide a factual and informative answer. "
            "Do not refer to any previous response.\n\n"
            f"Question: {question.strip()}"
        )

        # Generate each sample independently
        for i in range(number_of_samples):
            print(f"Generating sample {i + 1}/{number_of_samples}...")

            try:
                answer = self.gemini.generate_text(prompt)

                samples.append({
                    "sample_id": i + 1,
                    "answer": answer
                })

            except RuntimeError as exc:
                # Record the failure without losing successful samples
                errors.append({
                    "sample_id": i + 1,
                    "error": str(exc)
                })

                print(f"Sample {i + 1} failed: {exc}")

        # Determine the overall generation status
        if len(samples) == number_of_samples:
            status = "completed"
        elif len(samples) > 0:
            status = "partial"
        else:
            status = "failed"

        return {
            "question": question.strip(),
            "samples": samples,
            "sample_count": len(samples),
            "requested_samples": number_of_samples,
            "errors": errors,
            "status": status,
            "model": MODEL_NAME
        }
