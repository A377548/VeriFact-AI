
import pytest
from unittest.mock import patch
import torch

from hallucination_detection.bertscore_detector import BERTScoreDetector


def test_bertscore_returns_similarity_results():
    detector = BERTScoreDetector()

    fake_scores = (
        torch.tensor([0.90, 0.80]),
        torch.tensor([0.90, 0.80]),
        torch.tensor([0.90, 0.80])
    )

    with patch(
        "hallucination_detection.bertscore_detector.score",
        return_value=fake_scores
    ):
        result = detector.check(
            "The car is fast.",
            ["The automobile is fast.", "The vehicle moves quickly."]
        )

    assert result["sample_count"] == 2
    assert result["sample_similarities"] == [0.9, 0.8]
    assert result["average_similarity"] == 0.85
    assert result["disagreement_score"] == 0.15


def test_bertscore_rejects_empty_claim():
    detector = BERTScoreDetector()

    with pytest.raises(ValueError):
        detector.check("", ["Sample answer"])


def test_bertscore_rejects_empty_samples():
    detector = BERTScoreDetector()

    with pytest.raises(ValueError):
        detector.check("Original claim", [])
