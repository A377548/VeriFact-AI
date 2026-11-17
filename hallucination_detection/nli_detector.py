
from transformers import pipeline


class NLIDetector:
    """
    Evaluates the relationship between an original claim
    and independently generated sample answers.
    """

    MODEL_NAME = "cross-encoder/nli-deberta-v3-small"

    def __init__(self, model_name=MODEL_NAME):
        self.model_name = model_name

        self.classifier = pipeline(
            "text-classification",
            model=model_name,
            tokenizer=model_name,
            top_k=None
        )

    def check(self, original_claim: str, samples: list) -> dict:
        if not isinstance(original_claim, str) or not original_claim.strip():
            raise ValueError("Original claim cannot be empty.")

        if not isinstance(samples, list) or not samples:
            raise ValueError("At least one sample is required.")

        if not all(
            isinstance(sample, str) and sample.strip()
            for sample in samples
        ):
            raise ValueError("Every sample must be a non-empty string.")

        results = []

        for sample in samples:
            # Original claim is the hypothesis.
            # Sample answer is the premise.
            prediction = self.classifier({
                "text": sample.strip(),
                "text_pair": original_claim.strip()
            })

            scores = prediction[0]

            probabilities = {
                item["label"].lower(): float(item["score"])
                for item in scores
            }

            entailment = probabilities.get("entailment", 0.0)
            contradiction = probabilities.get("contradiction", 0.0)
            neutral = probabilities.get("neutral", 0.0)

            results.append({
                "sample": sample,
                "entailment": round(entailment, 4),
                "contradiction": round(contradiction, 4),
                "neutral": round(neutral, 4),
                "predicted_relation": max(
                    probabilities,
                    key=probabilities.get
                )
            })

        return {
            "detector": "NLI",
            "model": self.model_name,
            "sample_count": len(samples),
            "results": results
        }
