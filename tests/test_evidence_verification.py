
import unittest

from evidence_retrieval.evidence_verification_pipeline import (
    EvidenceVerificationPipeline
)


class MockRetrievalPipeline:

    def process(self, claims):
        results = []

        for claim in claims:
            results.append({
                "claim_id": claim["claim_id"],
                "claim": claim["claim"],
                "retrieved_count": 1,
                "evidence_count": 1,
                "evidence": [{
                    "evidence_id": "E001",
                    "source": "Test",
                    "title": "Test Evidence",
                    "url": "https://example.com",
                    "text": "Earth orbits the Sun."
                }],
                "status": "success"
            })

        return {
            "claim_count": len(claims),
            "results": results
        }


class MockNLIDetector:

    def check(self, claim, evidence):
        return {
            "evidence_count": len(evidence),
            "overall_relation": "supported",
            "relation_counts": {
                "entailment": 1,
                "contradiction": 0,
                "neutral": 0
            },
            "results": [{
                "evidence_id": "E001",
                "predicted_relation": "entailment"
            }]
        }


class TestEvidenceVerificationPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = EvidenceVerificationPipeline(
            retrieval_pipeline=MockRetrievalPipeline(),
            nli_detector=MockNLIDetector()
        )

    def test_combined_pipeline(self):
        result = self.pipeline.process([
            {
                "claim_id": "C001",
                "claim": "Earth revolves around the Sun."
            }
        ])

        self.assertEqual(result["claim_count"], 1)
        self.assertEqual(
            result["results"][0]["overall_relation"],
            "supported"
        )

    def test_claim_id_preservation(self):
        result = self.pipeline.process([
            {
                "claim_id": "C002",
                "claim": "Earth orbits the Sun."
            }
        ])

        self.assertEqual(
            result["results"][0]["claim_id"],
            "C002"
        )

    def test_empty_claims(self):
        result = self.pipeline.process([])

        self.assertEqual(result["claim_count"], 0)
        self.assertEqual(result["results"], [])


if __name__ == "__main__":
    unittest.main()
