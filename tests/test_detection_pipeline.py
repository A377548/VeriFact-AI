
from hallucination_detection.detection_pipeline import (
    HallucinationDetectionPipeline
)


class FakeSelfCheck:
    def check(self, claim, samples):
        return {
            "overall_risk_score": 0.2
        }


class FakeBERTScore:
    def check(self, claim, samples):
        return {
            "disagreement_score": 0.3
        }


class FakeNLI:
    def check(self, claim, samples):
        return {
            "results": [
                {"contradiction": 0.1},
                {"contradiction": 0.2}
            ]
        }


def test_pipeline_processes_claim_and_preserves_claim_id():
    pipeline = HallucinationDetectionPipeline(
        selfcheck=FakeSelfCheck(),
        bertscore=FakeBERTScore(),
        nli=FakeNLI()
    )

    input_data = {
        "question": "Who discovered penicillin?",
        "original_answer": "Alexander Fleming discovered penicillin.",
        "samples": [
            {
                "sample_id": 1,
                "answer": "Alexander Fleming discovered penicillin."
            },
            {
                "sample_id": 2,
                "answer": "Fleming discovered penicillin."
            }
        ],
        "claims": [
            {
                "claim_id": "C001",
                "claim": "Alexander Fleming discovered penicillin.",
                "is_valid": True,
                "issues": []
            }
        ]
    }

    result = pipeline.process(input_data)

    assert result["claim_count"] == 1
    assert result["results"][0]["claim_id"] == "C001"
    assert result["results"][0]["combined_score"]["risk_score"] == 21.0
    assert result["overall_risk_score"] == 21.0
