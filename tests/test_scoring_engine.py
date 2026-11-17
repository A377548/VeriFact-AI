
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

    assert result["risk_score"] == 55.0

    assert result["risk_components"]["selfcheck"] == 0.60
    assert result["risk_components"]["bertscore"] == 0.30
    assert result["risk_components"]["nli"] == 0.70


def test_scoring_engine_accepts_custom_weights():
    engine = HallucinationScoringEngine({
        "selfcheck": 0.50,
        "bertscore": 0.25,
        "nli": 0.25
    })

    selfcheck = {"overall_risk_score": 1.0}
    bertscore = {"disagreement_score": 0.0}
    nli = {"results": [{"contradiction": 0.0}]}

    result = engine.calculate_score(
        selfcheck,
        bertscore,
        nli
    )

    assert result["risk_score"] == 50.0


def test_scoring_engine_rejects_invalid_weights():
    with pytest.raises(ValueError):
        HallucinationScoringEngine({
            "selfcheck": -0.1,
            "bertscore": 0.5,
            "nli": 0.6
        })


def test_scoring_engine_rejects_invalid_risk_score():
    engine = HallucinationScoringEngine()

    with pytest.raises(ValueError):
        engine.calculate_score(
            {"overall_risk_score": 1.5},
            {"disagreement_score": 0.3},
            {"results": [{"contradiction": 0.5}]}
        )


def test_scoring_engine_rejects_empty_nli_results():
    engine = HallucinationScoringEngine()

    with pytest.raises(ValueError):
        engine.calculate_score(
            {"overall_risk_score": 0.5},
            {"disagreement_score": 0.4},
            {"results": []}
        )
