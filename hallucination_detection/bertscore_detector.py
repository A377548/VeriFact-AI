
from bert_score import BERTScorer


class BERTScoreDetector:
    """
    Measures semantic similarity between an original claim
    and independently generated sample answers.

    Reuses one BERTScorer instance to avoid repeatedly
    loading the underlying language model.
    """

    def __init__(self, model_type="roberta-base", lang="en"):
        self.model_type = model_type
        self.lang = lang
        self._scorer = None

    def _get_scorer(self):
        """Create the scorer only once and reuse it."""
        if self._scorer is None:
            self._scorer = BERTScorer(
                model_type=self.model_type,
                lang=self.lang,
                rescale_with_baseline=False
            )

        return self._scorer

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

        scorer = self._get_scorer()

        precision, recall, f1 = scorer.score(
            predictions,
            references
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
