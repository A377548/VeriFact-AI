
from hallucination_detection.selfcheck import SelfCheckDetector


def test_selfcheck_detects_low_word_overlap():
    detector = SelfCheckDetector()

    original = "The Eiffel Tower is located in Berlin."

    samples = [
        "The Eiffel Tower is located in Paris.",
        "The Eiffel Tower stands in Paris.",
        "The Eiffel Tower is a landmark in France."
    ]

    result = detector.check(original, samples)

    assert result["sentence_count"] == 1
    assert result["sample_count"] == 3
    assert result["overall_risk_score"] > 0


def test_selfcheck_identical_answers_have_zero_risk():
    detector = SelfCheckDetector()

    original = "The Earth revolves around the Sun."

    samples = [
        "The Earth revolves around the Sun.",
        "The Earth revolves around the Sun."
    ]

    result = detector.check(original, samples)

    assert result["overall_risk_score"] == 0


def test_selfcheck_rejects_empty_original_answer():
    detector = SelfCheckDetector()

    try:
        detector.check("", ["Sample answer"])
        assert False, "Expected ValueError"
    except ValueError:
        pass
