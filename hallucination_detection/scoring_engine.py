
import math


class HallucinationScoringEngine:
    """
    Combines SelfCheck, BERTScore and NLI outputs
    into an experimental hallucination-risk score.

    The score is not a probability that a claim is false.
    """

    DEFAULT_WEIGHTS = {
        "selfcheck": 0.30,
        "bertscore": 0.30,
        "nli": 0.40
    }

    def __init__(self, weights=None):
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()

        if set(self.weights) != set(self.DEFAULT_WEIGHTS):
            raise ValueError(
                "Weights must contain selfcheck, bertscore and nli."
            )

        if any(
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < 0
            for value in self.weights.values()
        ):
            raise ValueError("Weights must be finite, non-negative numbers.")

        total = sum(self.weights.values())

        if total <= 0:
            raise ValueError("At least one weight must be positive.")

        # Normalize weights so that they sum to 1.
        self.weights = {
            name: value / total
            for name, value in self.weights.items()
        }

    @staticmethod
    def _validate_score(value, name):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
        ):
            raise ValueError(f"{name} must be a finite number.")

        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be between 0 and 1.")

        return float(value)

    def calculate_score(
        self,
        selfcheck_result: dict,
        bertscore_result: dict,
        nli_result: dict
    ) -> dict:
        """
        Calculate the combined experimental risk score.
        """

        if not all(
            isinstance(result, dict)
            for result in (
                selfcheck_result,
                bertscore_result,
                nli_result
            )
        ):
            raise ValueError("All detector results must be dictionaries.")

        # Extract SelfCheck disagreement.
        selfcheck_risk = self._validate_score(
            selfcheck_result.get("overall_risk_score"),
            "SelfCheck risk"
        )

        # Extract BERTScore disagreement.
        bertscore_risk = self._validate_score(
            bertscore_result.get("disagreement_score"),
            "BERTScore disagreement"
        )

        # Calculate average NLI contradiction probability.
        nli_results = nli_result.get("results")

        if not isinstance(nli_results, list) or not nli_results:
            raise ValueError("NLI results must contain at least one sample.")

        contradictions = []

        for item in nli_results:
            if not isinstance(item, dict):
                raise ValueError("Every NLI result must be a dictionary.")

            contradictions.append(
                self._validate_score(
                    item.get("contradiction"),
                    "NLI contradiction"
                )
            )

        nli_risk = sum(contradictions) / len(contradictions)

        # Calculate weighted combined risk.
        combined_risk = (
            self.weights["selfcheck"] * selfcheck_risk
            + self.weights["bertscore"] * bertscore_risk
            + self.weights["nli"] * nli_risk
        )

        return {
            "detector": "Combined Hallucination Scoring Engine",
            "risk_score": round(combined_risk * 100, 2),
            "risk_components": {
                "selfcheck": round(selfcheck_risk, 4),
                "bertscore": round(bertscore_risk, 4),
                "nli": round(nli_risk, 4)
            },
            "weights": {
                name: round(value, 4)
                for name, value in self.weights.items()
            },
            "interpretation": (
                "Experimental disagreement and contradiction score; "
                "not a calibrated probability of hallucination."
            )
        }
