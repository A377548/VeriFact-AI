
import re


class SelfCheckDetector:
    """
    Detects potential inconsistencies between an original answer
    and independently generated sample answers.

    This initial version uses word overlap as a simple baseline.
    It does not establish whether a claim is factually true.
    """

    def _split_sentences(self, text: str) -> list:
        """Split text into individual sentences."""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [sentence.strip() for sentence in sentences if sentence.strip()]

    def _tokenize(self, text: str) -> set:
        """Convert text into lowercase word tokens."""
        return set(re.findall(r'\b\w+\b', text.lower()))

    def _similarity(self, sentence: str, sample: str) -> float:
        """Calculate Jaccard word similarity."""
        sentence_words = self._tokenize(sentence)
        sample_words = self._tokenize(sample)

        if not sentence_words or not sample_words:
            return 0.0

        intersection = sentence_words.intersection(sample_words)
        union = sentence_words.union(sample_words)

        return len(intersection) / len(union)

    def check(self, original_answer: str, samples: list) -> dict:
        """
        Compare original answer sentences with independent samples.
        """

        if not isinstance(original_answer, str) or not original_answer.strip():
            raise ValueError("Original answer cannot be empty.")

        if not isinstance(samples, list):
            raise ValueError("Samples must be provided as a list.")

        if not samples:
            raise ValueError("At least one sample answer is required.")

        if not all(isinstance(sample, str) and sample.strip() for sample in samples):
            raise ValueError("Every sample must be a non-empty string.")

        sentences = self._split_sentences(original_answer)

        results = []

        for index, sentence in enumerate(sentences, start=1):
            similarities = [
                self._similarity(sentence, sample)
                for sample in samples
            ]

            average_similarity = sum(similarities) / len(similarities)

            risk_score = 1.0 - average_similarity

            results.append({
                "sentence_id": index,
                "sentence": sentence,
                "sample_similarities": similarities,
                "average_similarity": round(average_similarity, 4),
                "risk_score": round(risk_score, 4)
            })

        overall_risk = sum(
            item["risk_score"] for item in results
        ) / len(results) if results else 0.0

        return {
            "detector": "SelfCheck Baseline",
            "sentence_count": len(results),
            "sample_count": len(samples),
            "overall_risk_score": round(overall_risk, 4),
            "results": results
        }
