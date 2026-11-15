
from evaluation.claim_evaluator import ClaimEvaluator
from evaluation.reference_dataset import REFERENCE_DATASET


evaluator = ClaimEvaluator()

# Controlled predictions for testing the evaluator.
# These are not actual Gemini outputs.
predictions = {
    "E001": [
        "Alexander Fleming discovered penicillin.",
        "Penicillin was discovered in 1928.",
        "An unrelated incorrect claim."
    ],

    "E002": [
        "Marie Curie discovered polonium.",
        "Marie Curie discovered radium."
    ],

    "E003": [
        "The Eiffel Tower is located in Paris.",
        "The Eiffel Tower was completed in 1889."
    ]
}

result = evaluator.evaluate_dataset(
    REFERENCE_DATASET,
    predictions
)

print("\n--- Per-example Evaluation ---")

for example in result["examples"]:
    print("\nExample:", example["example_id"])

    for metric, value in example["metrics"].items():
        print(f"{metric}: {value}")

print("\n--- Overall Dataset Evaluation ---")

for key, value in result.items():
    if key != "examples":
        print(f"{key}: {value}")

assert result["total_true_positives"] == 6
assert result["total_false_positives"] == 1
assert result["total_false_negatives"] == 3

assert result["micro_precision"] == 0.8571
assert result["micro_recall"] == 0.6667
assert result["micro_f1_score"] == 0.75

print("\nComplete dataset evaluation test passed!")