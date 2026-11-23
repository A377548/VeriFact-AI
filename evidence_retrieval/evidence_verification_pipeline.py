
from evidence_retrieval.evidence_pipeline import EvidenceRetrievalPipeline
from hallucination_detection.evidence_nli_detector import EvidenceNLIDetector


class EvidenceVerificationPipeline:
    """
    Combines evidence retrieval, evidence ranking,
    and evidence-based NLI verification.
    """

    def __init__(
        self,
        retrieval_pipeline=None,
        nli_detector=None
    ):
        self.retrieval_pipeline = (
            retrieval_pipeline or EvidenceRetrievalPipeline()
        )

        self.nli_detector = nli_detector or EvidenceNLIDetector()

    def process(self, claims: list[dict]) -> dict:

        if not isinstance(claims, list):
            raise ValueError("Claims must be a list.")

        # Phase 5: Retrieve and rank evidence.
        retrieval_output = self.retrieval_pipeline.process(claims)

        verification_results = []

        for item in retrieval_output["results"]:

            claim_id = item["claim_id"]
            claim_text = item["claim"]
            evidence = item["evidence"]

            if not evidence:
                verification_results.append({
                    "claim_id": claim_id,
                    "claim": claim_text,
                    "evidence_count": 0,
                    "overall_relation": "insufficient_evidence",
                    "evidence": [],
                    "status": item["status"]
                })
                continue

            try:
                # Phase 6: Verify claim against retrieved evidence.
                nli_output = self.nli_detector.check(
                    claim=claim_text,
                    evidence=evidence
                )

                verification_results.append({
                    "claim_id": claim_id,
                    "claim": claim_text,
                    "evidence_count": nli_output["evidence_count"],
                    "overall_relation": nli_output["overall_relation"],
                    "relation_counts": nli_output["relation_counts"],
                    "evidence": nli_output["results"],
                    "status": "success"
                })

            except (ValueError, RuntimeError) as error:
                verification_results.append({
                    "claim_id": claim_id,
                    "claim": claim_text,
                    "evidence_count": 0,
                    "overall_relation": "verification_error",
                    "evidence": [],
                    "status": "verification_error",
                    "error": str(error)
                })

        return {
            "phase": "Phase 5 + Phase 6 - Evidence Verification",
            "claim_count": len(claims),
            "results": verification_results
        }
