
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

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
                "answer": (
                    "Alexander Fleming discovered penicillin."
                )
            },
            {
                "sample_id": 2,
                "answer": (
                    "Penicillin was discovered by Alexander Fleming."
                )
            },
            {
                "sample_id": 3,
                "answer": (
                    "Alexander Fleming discovered penicillin in 1928."
                )
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
        {
            "claim": "Alexander Fleming discovered penicillin in 1928.",
            "source_sentence_indices": [1]
        },
        {
            "claim": (
                "Alexander Fleming made the discovery "
                "at St. Mary's Hospital in London."
            ),
            "source_sentence_indices": [1, 2]
        }
    ]


def run_test():

    captured_output = StringIO()

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
        ),
        redirect_stdout(captured_output)
    ):
        main.main()

    output = captured_output.getvalue()

    # Verify the main application output
    assert "Alexander Fleming discovered penicillin" in output
    assert "Sample 1:" in output
    assert "Standardized VeriFact AI JSON" in output
    assert '"schema_version": "1.0"' in output
    assert '"claim_id": "C001"' in output
    assert '"claim_id": "C002"' in output
    assert '"valid_claim_count": 2' in output

    print(output)

    print("\nComplete main application integration test passed!")


if __name__ == "__main__":
    run_test()
