
from hallucination_detection.selfcheck import SelfCheckDetector
from hallucination_detection.bertscore_detector import BERTScoreDetector
from hallucination_detection.nli_detector import NLIDetector
from hallucination_detection.scoring_engine import HallucinationScoringEngine


class HallucinationDetectionPipeline:
    """
    Integrates all Person 2 detection methods.

    Accepts Person 1's standardized VeriFact AI output
    and returns claim-level consistency analysis.

    Risk scores are experimental signals, not probabilities
    that claims are factually false.
    """

    def __init__(
        self,
        selfcheck=None,
        bertscore=None,
        nli=None,
        scoring_engine=None
    ):
        self.selfcheck = selfcheck or SelfCheckDetector()
        self.bertscore = bertscore or BERTScoreDetector()
        self.nli = nli or NLIDetector()
        self.scoring_engine = (
            scoring_engine or HallucinationScoringEngine()
        )

    def process(self, input_data: dict) -> dict:
        """
        Process Person 1's standardized output.

        Required input fields:
        question, original_answer, samples, claims
        """

        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary.")

        required_fields = [
            "question",
            "original_answer",
            "samples",
            "claims"
        ]

        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"Missing required field: {field}")

        question = input_data["question"]
        original_answer = input_data["original_answer"]
        sample_records = input_data["samples"]
        claims = input_data["claims"]

        if not isinstance(question, str) or not question.strip():
            raise ValueError("Question cannot be empty.")

        if (
            not isinstance(original_answer, str)
            or not original_answer.strip()
        ):
            raise ValueError("Original answer cannot be empty.")

        if not isinstance(sample_records, list) or not sample_records:
            raise ValueError("At least one sample is required.")

        if not isinstance(claims, list):
            raise ValueError("Claims must be provided as a list.")

        samples = []

        for sample in sample_records:
            if not isinstance(sample, dict):
                raise ValueError("Each sample must be a dictionary.")

            answer = sample.get("answer")

            if not isinstance(answer, str) or not answer.strip():
                raise ValueError("Every sample must have a valid answer.")

            samples.append(answer.strip())

        claim_results = []

        for claim_data in claims:
            if not isinstance(claim_data, dict):
                raise ValueError("Each claim must be a dictionary.")

            claim_id = claim_data.get("claim_id")
            claim_text = claim_data.get("claim")

            if not isinstance(claim_id, str) or not claim_id.strip():
                raise ValueError("Every claim must have a claim_id.")

            if not isinstance(claim_text, str) or not claim_text.strip():
                raise ValueError(
                    f"Claim {claim_id} must contain valid text."
                )

            # 1. SelfCheck consistency analysis
            selfcheck_result = self.selfcheck.check(
                claim_text,
                samples
            )

            # 2. BERTScore semantic similarity
            bertscore_result = self.bertscore.check(
                claim_text,
                samples
            )

            # 3. NLI-based sample consistency analysis
            nli_result = self.nli.check(
                claim_text,
                samples
            )

            # 4. Combined experimental risk score
            combined_result = self.scoring_engine.calculate_score(
                selfcheck_result,
                bertscore_result,
                nli_result
            )

            claim_results.append({
                "claim_id": claim_id,
                "claim": claim_text,
                "is_valid": claim_data.get("is_valid"),
                "issues": claim_data.get("issues", []),
                "selfcheck": selfcheck_result,
                "bertscore": bertscore_result,
                "nli": nli_result,
                "combined_score": combined_result
            })

        risk_scores = [
            item["combined_score"]["risk_score"]
            for item in claim_results
        ]

        overall_risk = (
            sum(risk_scores) / len(risk_scores)
            if risk_scores else 0.0
        )

        return {
            "project": "VeriFact AI",
            "schema_version": input_data.get("schema_version", "1.0"),
            "detector": "Person 2 - Hallucination Detection",
            "question": question,
            "claim_count": len(claim_results),
            "overall_risk_score": round(overall_risk, 2),
            "results": claim_results,
            "interpretation": (
                "Experimental consistency and contradiction signals. "
                "These scores do not establish factual truth."
            )
        }
