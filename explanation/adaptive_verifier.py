
from evidence_retrieval.wikipedia_retriever import WikipediaRetriever
from evidence_retrieval.evidence_ranker import EvidenceRanker
from hallucination_detection.evidence_nli_detector import EvidenceNLIDetector


class AdaptiveEvidenceVerifier:
    """
    Performs adaptive evidence retrieval and verification.

    Workflow:
    1. Retrieve an initial set of passages.
    2. Rank and verify the initial evidence.
    3. Expand retrieval when the result is uncertain.
    4. Combine and deduplicate both retrieval rounds.
    5. Re-rank the combined evidence.
    6. Perform final NLI verification.

    Evidence relevance and NLI predictions are experimental signals.
    They do not independently establish factual truth.
    """

    def __init__(
        self,
        retriever=None,
        ranker=None,
        nli_detector=None,
        initial_limit=5,
        expanded_limit=10,
        initial_top_k=3,
        expanded_top_k=8
    ):
        self.retriever = retriever or WikipediaRetriever()
        self.ranker = ranker or EvidenceRanker()
        self.nli_detector = nli_detector or EvidenceNLIDetector()

        self.initial_limit = initial_limit
        self.expanded_limit = expanded_limit
        self.initial_top_k = initial_top_k
        self.expanded_top_k = expanded_top_k

    def _is_uncertain(self, result):

        if result["overall_relation"] == "insufficient_evidence":
            return True

        counts = result.get("relation_counts", {})

        entailment = counts.get("entailment", 0)
        contradiction = counts.get("contradiction", 0)
        neutral = counts.get("neutral", 0)

        if neutral >= entailment and neutral >= contradiction:
            return True

        if entailment > 0 and contradiction > 0:
            if abs(entailment - contradiction) <= 1:
                return True

        return False

    def _combine_evidence(self, initial_evidence, expanded_evidence):
        """
        Combines evidence from both retrieval rounds
        and removes duplicate URL-and-text pairs.
        """

        combined_evidence = []
        seen_evidence = set()

        for item in initial_evidence + expanded_evidence:

            if not isinstance(item, dict):
                continue

            text = item.get("text", "")

            if not isinstance(text, str) or not text.strip():
                continue

            url = item.get("url", "")

            evidence_key = (
                str(url).strip().lower(),
                text.strip().lower()
            )

            if evidence_key in seen_evidence:
                continue

            seen_evidence.add(evidence_key)
            combined_evidence.append(item)

        return combined_evidence

    def verify(self, claim_id, claim):

        if not isinstance(claim, str) or not claim.strip():
            raise ValueError("Claim cannot be empty.")

        if not isinstance(claim_id, str) or not claim_id.strip():
            raise ValueError("Claim ID cannot be empty.")

        # First retrieval attempt.
        initial_evidence = self.retriever.search(
            claim,
            limit=self.initial_limit
        )

        ranked_evidence = self.ranker.rank(
            claim,
            initial_evidence,
            top_k=self.initial_top_k
        )

        initial_result = self.nli_detector.check(
            claim,
            ranked_evidence
        )

        expanded = False
        final_result = initial_result
        final_evidence = ranked_evidence

        # Retrieve more evidence when the initial result is uncertain.
        if self._is_uncertain(initial_result):

            expanded = True

            additional_evidence = self.retriever.search(
                claim,
                limit=self.expanded_limit
            )

            expanded_evidence = self.ranker.rank(
                claim,
                additional_evidence,
                top_k=self.expanded_top_k
            )

            combined_evidence = self._combine_evidence(
                ranked_evidence,
                expanded_evidence
            )

            # Re-rank the complete evidence collection.
            final_evidence = self.ranker.rank(
                claim,
                combined_evidence,
                top_k=self.expanded_top_k
            )

            # Final NLI verification uses re-ranked evidence.
            final_result = self.nli_detector.check(
                claim,
                final_evidence
            )

        return {
            "claim_id": claim_id,
            "claim": claim,
            "initial_relation": initial_result["overall_relation"],
            "final_relation": final_result["overall_relation"],
            "expanded": expanded,
            "evidence_count": final_result["evidence_count"],
            "relation_counts": final_result["relation_counts"],
            "evidence": final_result["results"],
            "selected_evidence": final_evidence
        }

    def process(self, claims):

        if not isinstance(claims, list):
            raise ValueError("Claims must be a list.")

        results = []

        for item in claims:

            if not isinstance(item, dict):
                continue

            claim_id = item.get("claim_id")
            claim = item.get("claim")

            if not isinstance(claim_id, str) or not claim_id.strip():
                continue

            if not isinstance(claim, str) or not claim.strip():
                continue

            try:
                result = self.verify(claim_id, claim)
                result["status"] = "success"

            except Exception as error:
                result = {
                    "claim_id": claim_id,
                    "claim": claim,
                    "status": "verification_error",
                    "error": str(error)
                }

            results.append(result)

        return {
            "phase": "Phase 7 - Adaptive Evidence Verification",
            "claim_count": len(claims),
            "results": results
        }
