
from transformers import pipeline


class NLIDetector:
    """
    Evaluates the relationship between an original claim
    and independently generated sample answers.

    The detector predicts entailment, contradiction or neutral.
    These predictions are not proof of factual truth.
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

            # Normalize the output returned by Transformers.
            if isinstance(prediction, dict):
                scores = [prediction]

            elif isinstance(prediction, list) and prediction:
                if isinstance(prediction[0], list):
                    scores = prediction[0]
                else:
                    scores = prediction

            else:
                raise ValueError(
                    "Unexpected NLI model output format."
                )

            if not all(isinstance(item, dict) for item in scores):
                raise ValueError(
                    "NLI model returned an invalid prediction format."
                )

            probabilities = {}

            for item in scores:
                label = item["label"].lower()

                # Handle generic labels such as LABEL_0 if returned.
                if label.startswith("label_"):
                    label_id = int(label.split("_")[1])
                    id2label = self.classifier.model.config.id2label
                    label = id2label.get(
                        label_id,
                        id2label.get(str(label_id), label)
                    ).lower()

                probabilities[label] = float(item["score"])

            required_labels = {
                "entailment",
                "contradiction",
                "neutral"
            }

            if not required_labels.issubset(probabilities):
                raise ValueError(
                    f"Unexpected NLI labels: {list(probabilities.keys())}"
                )

            entailment = probabilities["entailment"]
            contradiction = probabilities["contradiction"]
            neutral = probabilities["neutral"]

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
