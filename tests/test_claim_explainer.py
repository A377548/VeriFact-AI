
import unittest

from explanation.claim_explainer import ClaimExplainer


class TestClaimExplainer(unittest.TestCase):

    def setUp(self):
        self.explainer = ClaimExplainer()

    def test_supported_explanation(self):
        result = self.explainer.explain({
            "claim_id": "C001",
            "claim": "Earth orbits the Sun.",
            "overall_relation": "supported",
            "evidence": [
                {
                    "title": "Earth",
                    "source": "Wikipedia",
                    "url": "https://example.com",
                    "predicted_relation": "entailment"
                }
            ]
        })

        self.assertEqual(result["verdict"], "supported")
        self.assertEqual(result["claim_id"], "C001")
        self.assertEqual(result["evidence_count"], 1)

    def test_contradicted_explanation(self):
        result = self.explainer.explain({
            "claim_id": "C002",
            "claim": "The Sun revolves around Earth.",
            "overall_relation": "contradicted",
            "evidence": []
        })

        self.assertEqual(result["verdict"], "contradicted")

    def test_insufficient_evidence(self):
        result = self.explainer.explain({
            "claim_id": "C003",
            "claim": "A test claim.",
            "overall_relation": "insufficient_evidence",
            "evidence": []
        })

        self.assertEqual(
            result["verdict"],
            "insufficient_evidence"
        )

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.explainer.explain("invalid")

    def test_preserves_claim_id(self):
        result = self.explainer.explain({
            "claim_id": "C100",
            "claim": "Test claim.",
            "overall_relation": "supported",
            "evidence": []
        })

        self.assertEqual(result["claim_id"], "C100")


if __name__ == "__main__":
    unittest.main()
