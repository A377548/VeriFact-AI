
import pytest
from unittest.mock import patch, MagicMock
import torch

from hallucination_detection.bertscore_detector import BERTScoreDetector


def test_bertscore_returns_similarity_results():
    detector = BERTScoreDetector()

    fake_scores = (
        torch.tensor([0.90, 0.80]),
        torch.tensor([0.90, 0.80]),
        torch.tensor([0.90, 0.80])
    )

    fake_scorer = MagicMock()
    fake_scorer.score.return_value = fake_scores

    with patch(
        "hallucination_detection.bertscore_detector.BERTScorer",
        return_value=fake_scorer
    ) as mock_constructor:

        result = detector.check(
            "The car is fast.",
            ["The automobile is fast.", "The vehicle moves quickly."]
        )

    assert result["sample_count"] == 2
    assert result["sample_similarities"] == [0.9, 0.8]
    assert result["average_similarity"] == 0.85
    assert result["disagreement_score"] == 0.15

    mock_constructor.assert_called_once()
    fake_scorer.score.assert_called_once()


def test_bertscore_reuses_scorer():
    detector = BERTScoreDetector()

    fake_scorer = MagicMock()
    fake_scorer.score.return_value = (
        torch.tensor([0.9]),
        torch.tensor([0.9]),
        torch.tensor([0.9])
    )

    with patch(
        "hallucination_detection.bertscore_detector.BERTScorer",
        return_value=fake_scorer
    ) as mock_constructor:

        detector.check("Original claim", ["Sample one"])
        detector.check("Another claim", ["Sample two"])

    mock_constructor.assert_called_once()
    assert fake_scorer.score.call_count == 2


def test_bertscore_rejects_empty_claim():
    detector = BERTScoreDetector()

    with pytest.raises(ValueError):
        detector.check("", ["Sample answer"])


def test_bertscore_rejects_empty_samples():
    detector = BERTScoreDetector()

    with pytest.raises(ValueError):
        detector.check("Original claim", [])
