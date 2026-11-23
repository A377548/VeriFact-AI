
import unittest

from explanation.adaptive_verifier import AdaptiveEvidenceVerifier


class MockRetriever:

    def __init__(self):
        self.calls = []

    def search(self, claim, limit=5):
        self.calls.append(limit)

        return [
            {
                "evidence_id": f"E{i}",
                "source": "Test",
                "title": f"Evidence {i}",
                "url": "https://example.com",
                "text": f"Evidence passage number {i} about the claim."
            }
            for i in range(1, limit + 1)
        ]


class MockRanker:

    def rank(self, claim, evidence, top_k=3):
        return evidence[:top_k]


class MockNLIDetector:

    def __init__(self):
        self.calls = 0

    def check(self, claim, evidence):
        self.calls += 1

        if self.calls == 1:
            return {
                "overall_relation": "insufficient_evidence",
                "evidence_count": len(evidence),
                "relation_counts": {
                    "entailment": 0,
                    "contradiction": 0,
                    "neutral": len(evidence)
                },
                "results": []
            }

        return {
            "overall_relation": "supported",
            "evidence_count": len(evidence),
            "relation_counts": {
                "entailment": len(evidence),
                "contradiction": 0,
                "neutral": 0
            },
            "results": []
        }


class TestAdaptiveVerifier(unittest.TestCase):

    def setUp(self):
        self.retriever = MockRetriever()
        self.nli = MockNLIDetector()

        self.verifier = AdaptiveEvidenceVerifier(
            retriever=self.retriever,
            ranker=MockRanker(),
            nli_detector=self.nli
        )

    def test_adaptive_expansion(self):

        result = self.verifier.verify(
            "C001",
            "Earth revolves around the Sun."
        )

        self.assertTrue(result["expanded"])
        self.assertEqual(result["initial_relation"],
                         "insufficient_evidence")
        self.assertEqual(result["final_relation"], "supported")

    def test_retrieval_expands(self):

        self.verifier.verify(
            "C002",
            "A test claim."
        )

        self.assertEqual(self.retriever.calls, [5, 10])

    def test_claim_id_preservation(self):

        result = self.verifier.verify(
            "C003",
            "A test claim."
        )

        self.assertEqual(result["claim_id"], "C003")

    def test_process(self):

        result = self.verifier.process([
            {
                "claim_id": "C004",
                "claim": "A test claim."
            }
        ])

        self.assertEqual(result["claim_count"], 1)
        self.assertEqual(result["results"][0]["status"], "success")


if __name__ == "__main__":
    unittest.main()
