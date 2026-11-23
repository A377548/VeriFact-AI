
import unittest

from hallucination_detection.evidence_nli_detector import (
    EvidenceNLIDetector
)


class MockClassifier:

    def __init__(self, relations=None):
        self.relations = relations or ["entailment"]
        self.calls = 0

    def __call__(self, inputs):

        relation = self.relations[
            min(self.calls, len(self.relations) - 1)
        ]
        self.calls += 1

        scores = {
            "entailment": 0.85,
            "contradiction": 0.05,
            "neutral": 0.10
        }

        if relation == "contradiction":
            scores = {
                "entailment": 0.05,
                "contradiction": 0.85,
                "neutral": 0.10
            }

        elif relation == "neutral":
            scores = {
                "entailment": 0.10,
                "contradiction": 0.10,
                "neutral": 0.80
            }

        return [[
            {"label": key, "score": value}
            for key, value in scores.items()
        ]]


class TestEvidenceNLIDetector(unittest.TestCase):

    def create_detector(self, relations=None):
        return EvidenceNLIDetector(
            classifier=MockClassifier(relations)
        )

    def test_supported_claim_from_two_publishers(self):

        detector = self.create_detector()

        evidence = [
            {
                "evidence_id": "E001",
                "url": "https://science.org/article1",
                "text": "Earth orbits the Sun."
            },
            {
                "evidence_id": "E002",
                "url": "https://nature.com/article2",
                "text": "Earth revolves around the Sun."
            }
        ]

        result = detector.check(
            "Earth revolves around the Sun.",
            evidence
        )

        self.assertEqual(result["overall_relation"], "supported")
        self.assertEqual(result["evidence_count"], 2)
        self.assertEqual(
            result["independent_sources"]["entailment"], 2
        )

    def test_empty_evidence(self):

        result = self.create_detector().check(
            "Earth revolves around the Sun.",
            []
        )

        self.assertEqual(
            result["overall_relation"],
            "insufficient_evidence"
        )

    def test_invalid_claim(self):

        with self.assertRaises(ValueError):
            self.create_detector().check("", [])

    def test_preserves_evidence_id(self):

        evidence = [{
            "evidence_id": "E123",
            "text": "Earth orbits the Sun."
        }]

        result = self.create_detector().check(
            "Earth revolves around the Sun.",
            evidence
        )

        self.assertEqual(
            result["results"][0]["evidence_id"], "E123"
        )

    def test_single_source_is_insufficient(self):

        evidence = [{
            "evidence_id": "E001",
            "url": "https://science.org/article1",
            "text": "Earth orbits the Sun."
        }]

        result = self.create_detector().check(
            "Earth revolves around the Sun.",
            evidence
        )

        self.assertEqual(
            result["overall_relation"],
            "insufficient_evidence"
        )

    def test_same_publisher_different_urls_count_once(self):

        evidence = [
            {
                "evidence_id": "E001",
                "url": "https://en.wikipedia.org/wiki/Earth",
                "text": "Earth orbits the Sun."
            },
            {
                "evidence_id": "E002",
                "url": "https://en.wikipedia.org/wiki/Solar_System",
                "text": "Earth revolves around the Sun."
            }
        ]

        result = self.create_detector().check(
            "Earth revolves around the Sun.",
            evidence
        )

        self.assertEqual(
            result["overall_relation"],
            "insufficient_evidence"
        )

        self.assertEqual(
            result["independent_sources"]["entailment"], 1
        )

    def test_conflicting_passages_from_same_publisher(self):

        detector = self.create_detector([
            "entailment",
            "contradiction"
        ])

        evidence = [
            {
                "evidence_id": "E001",
                "url": "https://example.org/article1",
                "text": "Supporting passage."
            },
            {
                "evidence_id": "E002",
                "url": "https://example.org/article2",
                "text": "Conflicting passage."
            }
        ]

        result = detector.check("Test claim.", evidence)

        self.assertEqual(
            result["overall_relation"],
            "insufficient_evidence"
        )

        self.assertEqual(
            result["independent_sources"]["entailment"], 0
        )

        self.assertEqual(
            result["independent_sources"]["contradiction"], 0
        )

    def test_same_publisher_does_not_count_twice(self):

        evidence = [
            {
                "evidence_id": "E001",
                "url": "https://example.com/article1",
                "text": "First passage."
            },
            {
                "evidence_id": "E002",
                "url": "https://example.com/article2",
                "text": "Second passage."
            }
        ]

        result = self.create_detector().check(
            "Test claim.", evidence
        )

        self.assertEqual(
            result["independent_sources"]["entailment"], 1
        )

        self.assertEqual(
            result["overall_relation"],
            "insufficient_evidence"
        )


if __name__ == "__main__":
    unittest.main()
