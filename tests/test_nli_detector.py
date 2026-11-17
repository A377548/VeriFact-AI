
import pytest
from unittest.mock import patch

from hallucination_detection.nli_detector import NLIDetector


def test_nli_returns_relationship_scores():
    fake_prediction = [[
        {"label": "entailment", "score": 0.85},
        {"label": "contradiction", "score": 0.05},
        {"label": "neutral", "score": 0.10}
    ]]

    with patch(
        "hallucination_detection.nli_detector.pipeline"
    ) as mock_pipeline:

        mock_classifier = mock_pipeline.return_value
        mock_classifier.return_value = fake_prediction

        detector = NLIDetector()
        result = detector.check(
            "Paris is the capital of France.",
            ["Paris is in France."]
        )

    assert result["sample_count"] == 1

    item = result["results"][0]

    assert item["entailment"] == 0.85
    assert item["contradiction"] == 0.05
    assert item["neutral"] == 0.10


def test_nli_rejects_empty_claim():
    with patch("hallucination_detection.nli_detector.pipeline"):
        detector = NLIDetector()

    with pytest.raises(ValueError):
        detector.check("", ["Sample answer"])


def test_nli_rejects_empty_samples():
    with patch("hallucination_detection.nli_detector.pipeline"):
        detector = NLIDetector()

    with pytest.raises(ValueError):
        detector.check("Original claim", [])
