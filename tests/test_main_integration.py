
from unittest.mock import patch

import main


def fake_original_response(question):
    return {
        "question": question,
        "answer": (
            "Alexander Fleming discovered penicillin in 1928. "
            "He made the discovery at St. Mary's Hospital in London."
        ),
        "model": "simulated-model"
    }


def fake_samples(question, number_of_samples=3):
    return {
        "question": question,
        "samples": [
            {
                "sample_id": 1,
                "answer": "Alexander Fleming discovered penicillin."
            },
            {
                "sample_id": 2,
                "answer": "Penicillin was discovered by Alexander Fleming."
            },
            {
                "sample_id": 3,
                "answer": "Alexander Fleming discovered penicillin in 1928."
            }
        ],
        "sample_count": 3,
        "requested_samples": number_of_samples,
        "errors": [],
        "status": "completed",
        "model": "simulated-model"
    }


def fake_claim_extraction(answer):
    return [
        "Alexander Fleming discovered penicillin.",
        "Penicillin was discovered in 1928.",
        "Alexander Fleming made the discovery at St. Mary's Hospital.",
        "St. Mary's Hospital is located in London."
    ]


def run_test():
    with (
        patch(
            "builtins.input",
            return_value="Who discovered penicillin?"
        ),
        patch(
            "main.ResponseGenerator.generate_original_response",
            side_effect=fake_original_response
        ),
        patch(
            "main.SampleGenerator.generate_samples",
            side_effect=fake_samples
        ),
        patch(
            "claim_extraction.claim_pipeline.AtomicClaimExtractor.extract_claims",
            side_effect=fake_claim_extraction
        )
    ):
        main.main()


if __name__ == "__main__":
    run_test()
