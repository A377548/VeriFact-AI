
import math


class HallucinationScoringEngine:
    """
    Combines SelfCheck and BERTScore into an experimental
    hallucination-risk score.

    NLI is retained as a diagnostic signal but excluded from
    the default combined score because its reliability has
    not yet been adequately validated.

    The score is not a probability that a claim is false.
    """

    DEFAULT_WEIGHTS = {
        "selfcheck": 0.50,
        "bertscore": 0.50,
        "nli": 0.00
    }

    def __init__(self, weights=None):
        self.weights = (
            weights.copy()
            if weights is not None
            else self.DEFAULT_WEIGHTS.copy()
        )

        if not isinstance(self.weights, dict):
            raise ValueError("Weights must be a dictionary.")

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
            raise ValueError(
                "Weights must be finite, non-negative numbers."
            )

        total = sum(self.weights.values())

        if total <= 0:
            raise ValueError("At least one weight must be positive.")

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

        NLI contradiction is reported separately and does not
        affect the default combined score.
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

        selfcheck_risk = self._validate_score(
            selfcheck_result.get("overall_risk_score"),
            "SelfCheck risk"
        )

        bertscore_risk = self._validate_score(
            bertscore_result.get("disagreement_score"),
            "BERTScore disagreement"
        )

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
                "Experimental disagreement score based on SelfCheck "
                "and BERTScore by default. NLI is reported separately "
                "as an experimental diagnostic signal. This is not "
                "a calibrated probability of hallucination."
            )
        }
