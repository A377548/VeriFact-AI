
class ClaimExplainer:
    """
    Generates explanations for evidence-based claim verification.
    Explanations are based on actual NLI predictions and retrieved evidence.
    """

    def explain(self, verification_result: dict) -> dict:

        if not isinstance(verification_result, dict):
            raise ValueError("Verification result must be a dictionary.")

        claim = verification_result.get("claim", "")
        relation = verification_result.get(
            "overall_relation",
            "insufficient_evidence"
        )

        evidence = verification_result.get("evidence", [])

        if not isinstance(evidence, list):
            evidence = []

        if relation == "supported":
            explanation = (
                "The retrieved evidence contains passages that "
                "the NLI model identifies as supporting this claim."
            )

        elif relation == "contradicted":
            explanation = (
                "The retrieved evidence contains passages that "
                "the NLI model identifies as contradicting this claim."
            )

        elif relation == "verification_error":
            explanation = (
                "Evidence was retrieved, but the verification "
                "process encountered an error."
            )

        else:
            explanation = (
                "The available evidence is insufficient to "
                "establish whether this claim is true or false."
            )

        evidence_summaries = []

        for item in evidence:

            if not isinstance(item, dict):
                continue

            evidence_summaries.append({
                "title": item.get("title"),
                "source": item.get("source"),
                "url": item.get("url"),
                "relation": item.get("predicted_relation"),
                "entailment": item.get("entailment"),
                "contradiction": item.get("contradiction"),
                "neutral": item.get("neutral")
            })

        return {
            "claim_id": verification_result.get("claim_id"),
            "claim": claim,
            "verdict": relation,
            "explanation": explanation,
            "evidence_count": len(evidence_summaries),
            "evidence_summaries": evidence_summaries
        }
