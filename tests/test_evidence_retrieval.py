
import unittest

from evidence_retrieval.evidence_pipeline import (
    EvidenceRetrievalPipeline
)
from evidence_retrieval.evidence_ranker import EvidenceRanker


class MockRetriever:
    def search(self, claim):
        return [
            {
                "evidence_id": "E001",
                "source": "Test",
                "title": "Earth",
                "url": "https://example.com/earth",
                "text": "Earth revolves around the Sun."
            },
            {
                "evidence_id": "E002",
                "source": "Test",
                "title": "Moon",
                "url": "https://example.com/moon",
                "text": "The Moon orbits the Earth."
            }
        ]


class TestEvidenceRetrieval(unittest.TestCase):

    def test_evidence_ranking(self):
        evidence = [
            {"title": "Earth", "text": "Earth revolves around the Sun."},
            {"title": "Moon", "text": "The Moon orbits the Earth."}
        ]

        ranked = EvidenceRanker().rank(
            "Earth revolves around the Sun",
            evidence,
            top_k=2
        )

        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0]["title"], "Earth")
        self.assertGreater(
            ranked[0]["relevance_score"],
            ranked[1]["relevance_score"]
        )

    def test_pipeline_preserves_claim_id(self):
        pipeline = EvidenceRetrievalPipeline(
            retriever=MockRetriever()
        )

        result = pipeline.process([
            {
                "claim_id": "C001",
                "claim": "Earth revolves around the Sun."
            }
        ])

        self.assertEqual(result["claim_count"], 1)
        self.assertEqual(
            result["results"][0]["claim_id"],
            "C001"
        )
        self.assertEqual(
            result["results"][0]["status"],
            "success"
        )

    def test_empty_evidence(self):
        class EmptyRetriever:
            def search(self, claim):
                return []

        pipeline = EvidenceRetrievalPipeline(
            retriever=EmptyRetriever()
        )

        result = pipeline.process([
            {
                "claim_id": "C002",
                "claim": "A test claim."
            }
        ])

        self.assertEqual(
            result["results"][0]["status"],
            "no_evidence_found"
        )


if __name__ == "__main__":
    unittest.main()
