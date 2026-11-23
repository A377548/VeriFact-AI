
from urllib.parse import urlparse


class EvidenceNLIDetector:
    """
    Evidence-based Natural Language Inference detector.

    Uses confidence thresholds and publisher-level grouping
    to produce conservative fact-checking verdicts.

    Different URLs from the same publisher count as one
    publisher, not multiple independent sources.
    """

    MODEL_NAME = "cross-encoder/nli-deberta-v3-small"

    MIN_RELEVANCE_SCORE = 0.01
    MIN_ENTAILMENT_CONFIDENCE = 0.80
    MIN_CONTRADICTION_CONFIDENCE = 0.80

    MIN_INDEPENDENT_SOURCES = 2

    def __init__(self, model_name=MODEL_NAME, classifier=None):

        self.model_name = model_name

        if classifier is not None:
            self.classifier = classifier

        else:
            try:
                from transformers import pipeline

                self.classifier = pipeline(
                    "text-classification",
                    model=model_name,
                    tokenizer=model_name,
                    top_k=None
                )

            except Exception as error:
                raise RuntimeError(
                    "Unable to load the NLI model. "
                    "Check the Transformers installation."
                ) from error

    def _normalize_predictions(self, prediction):

        if isinstance(prediction, dict):
            scores = [prediction]

        elif isinstance(prediction, list) and prediction:

            if isinstance(prediction[0], list):
                scores = prediction[0]
            else:
                scores = prediction

        else:
            raise ValueError("Unexpected NLI model output.")

        probabilities = {}

        for item in scores:

            if not isinstance(item, dict):
                raise ValueError("Invalid NLI prediction.")

            label = item["label"].lower()

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

        return probabilities

    def _get_source_key(self, item):
        """
        Identify the publisher using the URL hostname.

        Multiple articles from the same domain count as
        one publisher. This is a publisher-diversity
        approximation, not proof of source independence.
        """

        url = item.get("url")

        if isinstance(url, str) and url.strip():

            try:
                parsed = urlparse(url.strip())

                hostname = (parsed.hostname or "").lower()

                if hostname.startswith("www."):
                    hostname = hostname[4:]

                if hostname:
                    return hostname

            except ValueError:
                pass

        source = item.get("source")

        if isinstance(source, str) and source.strip():
            return source.strip().lower()

        title = item.get("title")

        if isinstance(title, str) and title.strip():
            return title.strip().lower()

        evidence_id = item.get("evidence_id")

        if evidence_id:
            return str(evidence_id)

        return None

    def check(self, claim: str, evidence: list) -> dict:

        if not isinstance(claim, str) or not claim.strip():
            raise ValueError("Claim cannot be empty.")

        if not isinstance(evidence, list):
            raise ValueError("Evidence must be a list.")

        results = []

        for item in evidence:

            if not isinstance(item, dict):
                continue

            evidence_text = item.get("text")

            if not isinstance(evidence_text, str):
                continue

            if not evidence_text.strip():
                continue

            relevance_score = item.get("relevance_score", 1.0)

            try:
                relevance_score = float(relevance_score)

            except (TypeError, ValueError):
                relevance_score = 0.0

            if relevance_score < self.MIN_RELEVANCE_SCORE:
                continue

            prediction = self.classifier({
                "text": evidence_text.strip(),
                "text_pair": claim.strip()
            })

            probabilities = self._normalize_predictions(prediction)

            predicted_relation = max(
                probabilities,
                key=probabilities.get
            )

            results.append({
                "evidence_id": item.get("evidence_id"),
                "source": item.get("source"),
                "title": item.get("title"),
                "url": item.get("url"),
                "relevance_score": round(relevance_score, 4),
                "entailment": round(probabilities["entailment"], 4),
                "contradiction": round(probabilities["contradiction"], 4),
                "neutral": round(probabilities["neutral"], 4),
                "predicted_relation": predicted_relation,
                "source_key": self._get_source_key(item)
            })

        relation_counts = {
            "entailment": 0,
            "contradiction": 0,
            "neutral": 0
        }

        source_relations = {}

        for result in results:

            entailment_score = result["entailment"]
            contradiction_score = result["contradiction"]

            if (
                entailment_score >= self.MIN_ENTAILMENT_CONFIDENCE
                and entailment_score > contradiction_score
            ):
                relation = "entailment"

            elif (
                contradiction_score >= self.MIN_CONTRADICTION_CONFIDENCE
                and contradiction_score > entailment_score
            ):
                relation = "contradiction"

            else:
                relation = "neutral"

            relation_counts[relation] += 1
            result["confidence_relation"] = relation

            source_key = result["source_key"]

            if source_key is None:
                continue

            source_relations.setdefault(
                source_key,
                {
                    "entailment": 0,
                    "contradiction": 0
                }
            )

            if relation in ("entailment", "contradiction"):
                source_relations[source_key][relation] += 1

        independent_sources = {
            "entailment": 0,
            "contradiction": 0
        }

        for source_result in source_relations.values():

            if (
                source_result["entailment"] > 0
                and source_result["contradiction"] == 0
            ):
                independent_sources["entailment"] += 1

            elif (
                source_result["contradiction"] > 0
                and source_result["entailment"] == 0
            ):
                independent_sources["contradiction"] += 1

        entailment_sources = independent_sources["entailment"]
        contradiction_sources = independent_sources["contradiction"]

        if (
            entailment_sources >= self.MIN_INDEPENDENT_SOURCES
            and contradiction_sources == 0
        ):
            overall_relation = "supported"

        elif (
            contradiction_sources >= self.MIN_INDEPENDENT_SOURCES
            and entailment_sources == 0
        ):
            overall_relation = "contradicted"

        else:
            overall_relation = "insufficient_evidence"

        return {
            "detector": "Evidence-based NLI",
            "model": self.model_name,
            "claim": claim,
            "evidence_count": len(results),
            "relation_counts": relation_counts,
            "independent_sources": independent_sources,
            "overall_relation": overall_relation,
            "results": results
        }
