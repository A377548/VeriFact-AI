
from schemas.output_builder import OutputBuilder


# Mock original answer generation result
original_result = {
    "question": "Who discovered penicillin?",
    "answer": (
        "Alexander Fleming discovered penicillin in 1928."
    ),
    "model": "gemini-3.8-flash"
}


# Mock independent sample generation result
sample_result = {
    "samples": [
        {
            "sample_id": 1,
            "answer": "Alexander Fleming discovered penicillin in 1928."
        },
        {
            "sample_id": 2,
            "answer": "Penicillin was discovered by Alexander Fleming."
        },
        {
            "sample_id": 3,
            "answer": "Alexander Fleming identified penicillin in 1928."
        }
    ]
}


# Mock claim extraction result
claim_result = {
    "sentence_count": 1,
    "claim_count": 1,
    "valid_claim_count": 1,
    "invalid_claim_count": 0,
    "claims": [
        {
            "claim_id": "C001",
            "claim": "Alexander Fleming discovered penicillin.",
            "source_sentence_indices": [1],
            "source_sentences": [
                "Alexander Fleming discovered penicillin in 1928."
            ],
            "entities": [
                {
                    "text": "Alexander Fleming",
                    "label": "PERSON",
                    "description": "Person"
                }
            ],
            "is_valid": True,
            "issues": []
        }
    ]
}


# Build the complete output
builder = OutputBuilder()

result = builder.build_output(
    question="Who discovered penicillin?",
    original_result=original_result,
    sample_result=sample_result,
    claim_result=claim_result
)


# Display the validated JSON
print("\n--- Complete VeriFact AI Output ---")
print(result.model_dump_json(indent=4))


# Verify important fields
assert result.question == "Who discovered penicillin?"
assert len(result.samples) == 3
assert len(result.claims) == 1
assert result.claims[0].claim_id == "C001"
assert result.claim_summary.valid_claim_count == 1

print("\nOutput builder integration test passed!")

from pydantic import ValidationError


# Test whether invalid claim data is rejected
invalid_claim_result = {
    "sentence_count": 1,
    "claim_count": 1,
    "valid_claim_count": 1,
    "invalid_claim_count": 0,
    "claims": [
        {
            # claim_id intentionally missing
            "claim": "Alexander Fleming discovered penicillin.",
            "source_sentence_indices": [1],
            "source_sentences": [
                "Alexander Fleming discovered penicillin in 1928."
            ],
            "entities": [],
            "is_valid": True,
            "issues": []
        }
    ]
}


try:
    builder.build_output(
        question="Who discovered penicillin?",
        original_result=original_result,
        sample_result=sample_result,
        claim_result=invalid_claim_result
    )

    print("FAILED: Invalid claim was accepted.")

except ValidationError:
    print("PASSED: Invalid claim was rejected.")


print("\nAll output builder tests completed!")
