
from bert_score import score


class BERTScoreDetector:
    """
    Measures semantic similarity between an original claim
    and independently generated sample answers.
    """

    def __init__(self, model_type="roberta-base", lang="en"):
        self.model_type = model_type
        self.lang = lang

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

        predictions = [original_claim.strip()] * len(samples)
        references = [sample.strip() for sample in samples]

        precision, recall, f1 = score(
            predictions,
            references,
            model_type=self.model_type,
            lang=self.lang,
            verbose=False
        )

        similarities = [round(value.item(), 4) for value in f1]

        average_similarity = sum(similarities) / len(similarities)

        return {
            "detector": "BERTScore",
            "sample_count": len(samples),
            "sample_similarities": similarities,
            "average_similarity": round(average_similarity, 4),
            "disagreement_score": round(1 - average_similarity, 4),
            "model_type": self.model_type
        }
