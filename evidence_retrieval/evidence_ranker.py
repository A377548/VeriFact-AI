
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EvidenceRanker:
    """
    Ranks evidence passages using TF-IDF similarity.

    Features:
    - Input validation
    - Duplicate passage removal
    - Minimum relevance filtering
    - Source diversity
    - Preservation of original evidence metadata

    Relevance scores measure textual similarity only.
    They do not establish factual support.
    """

    def __init__(self, max_per_source=2, min_relevance=0.0):

        if (
            not isinstance(max_per_source, int)
            or isinstance(max_per_source, bool)
            or max_per_source < 1
        ):
            raise ValueError(
                "max_per_source must be a positive integer."
            )

        if (
            not isinstance(min_relevance, (int, float))
            or isinstance(min_relevance, bool)
            or not 0 <= min_relevance <= 1
        ):
            raise ValueError(
                "min_relevance must be between 0 and 1."
            )

        self.max_per_source = max_per_source
        self.min_relevance = float(min_relevance)

    def _normalize_text(self, text):
        text = text.lower()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s]", "", text)
        return text.strip()

    def rank(self, claim, evidence, top_k=3):

        if not isinstance(claim, str) or not claim.strip():
            raise ValueError("Claim must be a non-empty string.")

        if not isinstance(evidence, list):
            raise ValueError("Evidence must be a list.")

        if (
            not isinstance(top_k, int)
            or isinstance(top_k, bool)
            or top_k < 1
        ):
            raise ValueError("top_k must be a positive integer.")

        valid_evidence = []
        seen_text = set()

        # Validate evidence and remove duplicate passages.
        for item in evidence:

            if not isinstance(item, dict):
                continue

            text = item.get("text")

            if not isinstance(text, str) or not text.strip():
                continue

            normalized = self._normalize_text(text)

            if not normalized or normalized in seen_text:
                continue

            seen_text.add(normalized)
            valid_evidence.append(item)

        if not valid_evidence:
            return []

        documents = [claim.strip()] + [
            item["text"] for item in valid_evidence
        ]

        try:
            vectorizer = TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 2),
                sublinear_tf=True
            )

            vectors = vectorizer.fit_transform(documents)

            similarities = cosine_similarity(
                vectors[0:1],
                vectors[1:]
            )[0]

        except ValueError:
            return []

        ranked_evidence = []

        # Calculate similarity and apply relevance threshold.
        for item, similarity in zip(
            valid_evidence,
            similarities
        ):

            score = float(similarity)

            if score < self.min_relevance:
                continue

            result = item.copy()
            result["relevance_score"] = round(score, 4)

            ranked_evidence.append(result)

        # Highest relevance first.
        ranked_evidence.sort(
            key=lambda item: item["relevance_score"],
            reverse=True
        )

        # Select passages while maintaining source diversity.
        selected = []
        source_counts = {}

        for item in ranked_evidence:

            source_name = (
                item.get("url")
                or item.get("title")
                or item.get("source")
                or item.get("evidence_id")
                or "unknown"
            )

            source_name = str(source_name).casefold()

            if source_counts.get(source_name, 0) >= self.max_per_source:
                continue

            selected.append(item)

            source_counts[source_name] = (
                source_counts.get(source_name, 0) + 1
            )

            if len(selected) >= top_k:
                break

        return selected
