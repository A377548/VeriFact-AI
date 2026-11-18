
import pytest

from hallucination_detection.scoring_engine import (
    HallucinationScoringEngine
)


def test_scoring_engine_calculates_weighted_risk():
    engine = HallucinationScoringEngine()

    selfcheck = {
        "overall_risk_score": 0.60
    }

    bertscore = {
        "disagreement_score": 0.30
    }

    nli = {
        "results": [
            {"contradiction": 0.80},
            {"contradiction": 0.60}
        ]
    }

    result = engine.calculate_score(
        selfcheck,
        bertscore,
        nli
    )

    assert result["risk_score"] == 45.0

    assert result["risk_components"]["selfcheck"] == 0.60
    assert result["risk_components"]["bertscore"] == 0.30
    assert result["risk_components"]["nli"] == 0.70

    assert result["weights"] == {
        "selfcheck": 0.5,
        "bertscore": 0.5,
        "nli": 0.0
    }


def test_scoring_engine_accepts_custom_weights():
    engine = HallucinationScoringEngine(
        weights={
            "selfcheck": 0.60,
            "bertscore": 0.30,
            "nli": 0.10
        }
    )

    assert round(engine.weights["selfcheck"], 2) == 0.60
    assert round(engine.weights["bertscore"], 2) == 0.30
    assert round(engine.weights["nli"], 2) == 0.10


def test_scoring_engine_rejects_invalid_weights():
    with pytest.raises(ValueError):
        HallucinationScoringEngine(
            weights={
                "selfcheck": -0.1,
                "bertscore": 0.5,
                "nli": 0.6
            }
        )


def test_scoring_engine_rejects_invalid_risk_score():
    engine = HallucinationScoringEngine()

    selfcheck = {
        "overall_risk_score": 1.5
    }

    bertscore = {
        "disagreement_score": 0.30
    }

    nli = {
        "results": [
            {"contradiction": 0.50}
        ]
    }

    with pytest.raises(ValueError):
        engine.calculate_score(
            selfcheck,
            bertscore,
            nli
        )


def test_scoring_engine_rejects_empty_nli_results():
    engine = HallucinationScoringEngine()

    selfcheck = {
        "overall_risk_score": 0.60
    }

    bertscore = {
        "disagreement_score": 0.30
    }

    nli = {
        "results": []
    }

    with pytest.raises(ValueError):
        engine.calculate_score(
            selfcheck,
            bertscore,
            nli
        )


def test_nli_does_not_affect_default_combined_risk():
    engine = HallucinationScoringEngine()

    selfcheck = {
        "overall_risk_score": 0.60
    }

    bertscore = {
        "disagreement_score": 0.30
    }

    nli_low = {
        "results": [
            {"contradiction": 0.10},
            {"contradiction": 0.20}
        ]
    }

    nli_high = {
        "results": [
            {"contradiction": 0.90},
            {"contradiction": 1.00}
        ]
    }

    result_low = engine.calculate_score(
        selfcheck,
        bertscore,
        nli_low
    )

    result_high = engine.calculate_score(
        selfcheck,
        bertscore,
        nli_high
    )

    # NLI scores are still reported separately.
    assert result_low["risk_components"]["nli"] == 0.15
    assert result_high["risk_components"]["nli"] == 0.95

    # NLI must not affect the default combined risk score.
    assert result_low["risk_score"] == result_high["risk_score"]
    assert result_low["risk_score"] == 45.0
