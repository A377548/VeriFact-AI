
import json
from pathlib import Path

from evaluation.reference_dataset import REFERENCE_DATASET
from evaluation.claim_evaluator import ClaimEvaluator

# Load the saved predictions produced by the actual claim extraction pipeline.
PREDICTIONS_FILE = Path("data/experiment3_predictions.json")

if not PREDICTIONS_FILE.exists():
    raise FileNotFoundError(
        "Predictions file not found. Create data/experiment3_predictions.json first."
    )

with PREDICTIONS_FILE.open("r", encoding="utf-8") as file:
    predictions = json.load(file)

evaluator = ClaimEvaluator()

# Evaluate only examples successfully processed by the pipeline.
completed_dataset = [
    example
    for example in REFERENCE_DATASET
    if example["example_id"] in predictions
]

if not completed_dataset:
    raise ValueError("No successfully processed examples found.")

results = evaluator.evaluate_dataset(
    completed_dataset,
    predictions
)

print("\n--- EXPERIMENT 3: CLAIM EXTRACTION PERFORMANCE ---")
print("Total dataset examples:", len(REFERENCE_DATASET))
print("Successfully evaluated:", len(completed_dataset))
print(
    "Number of reference claims:",
sum(
    len(item["reference_claims"])
    for item in completed_dataset
))

for example in results["examples"]:
    metrics = example["metrics"]
    print("\nExample:", example["example_id"])
    print("TP:", metrics["true_positives"])
    print("FP:", metrics["false_positives"])
    print("FN:", metrics["false_negatives"])
    print("Precision:", metrics["precision"])
    print("Recall:", metrics["recall"])
    print("F1-score:", metrics["f1_score"])

print("\n--- OVERALL MICRO-AVERAGED RESULTS ---")
print("Total TP:", results["total_true_positives"])
print("Total FP:", results["total_false_positives"])
print("Total FN:", results["total_false_negatives"])
print("Micro Precision:", results["micro_precision"])
print("Micro Recall:", results["micro_recall"])
print("Micro F1-score:", results["micro_f1_score"])
