
from evidence_retrieval.wikipedia_retriever import WikipediaRetriever
from evidence_retrieval.evidence_ranker import EvidenceRanker


class EvidenceRetrievalPipeline:
    """Retrieve and rank evidence for extracted claims."""

    def __init__(
        self,
        retriever=None,
        ranker=None,
        top_k=3
    ):
        self.retriever = retriever or WikipediaRetriever()
        self.ranker = ranker or EvidenceRanker()
        self.top_k = top_k

    def process(self, claims: list[dict]) -> dict:

        if not isinstance(claims, list):
            raise ValueError("Claims must be a list.")

        results = []

        for claim_data in claims:

            if not isinstance(claim_data, dict):
                continue

            claim_id = claim_data.get("claim_id")
            claim_text = claim_data.get("claim")

            if not claim_id or not isinstance(claim_text, str) or not claim_text.strip():
                continue

            try:
                retrieved = self.retriever.search(claim_text)

                ranked = self.ranker.rank(
                    claim=claim_text,
                    evidence=retrieved,
                    top_k=self.top_k
                )

                results.append({
                    "claim_id": claim_id,
                    "claim": claim_text,
                    "retrieved_count": len(retrieved),
                    "evidence_count": len(ranked),
                    "evidence": ranked,
                    "status": (
                        "success" if ranked
                        else "no_evidence_found"
                    )
                })

            except (RuntimeError, ValueError) as error:
                results.append({
                    "claim_id": claim_id,
                    "claim": claim_text,
                    "retrieved_count": 0,
                    "evidence_count": 0,
                    "evidence": [],
                    "status": "retrieval_error",
                    "error": str(error)
                })

        return {
            "phase": "Phase 5 - Evidence Retrieval",
            "claim_count": len(claims),
            "results": results
        }
