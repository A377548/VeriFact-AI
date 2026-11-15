
import json
from pathlib import Path

from evaluation.reference_dataset import REFERENCE_DATASET
from claim_extraction.claim_pipeline import ClaimExtractionPipeline

OUTPUT_FILE = Path("data/experiment3_predictions.json")
ERROR_FILE = Path("data/experiment3_errors.json")

# Resume from previously saved predictions if the script is run again.
if OUTPUT_FILE.exists():
    with OUTPUT_FILE.open("r", encoding="utf-8") as file:
        predictions = json.load(file)
else:
    predictions = {}

if ERROR_FILE.exists():
    with ERROR_FILE.open("r", encoding="utf-8") as file:
        errors = json.load(file)
else:
    errors = {}

pipeline = ClaimExtractionPipeline()

print("\n--- GENERATING EXPERIMENT 3 PREDICTIONS ---")

for example in REFERENCE_DATASET:
    example_id = example["example_id"]

    # Skip examples that have already been processed successfully.
    if example_id in predictions:
        print(f"{example_id}: Already processed. Skipping.")
        continue

    print(f"\nProcessing {example_id}...")

    try:
        result = pipeline.process_answer(example["answer"])

        extracted_claims = [
            claim["claim"]
            for claim in result["claims"]
        ]

        predictions[example_id] = extracted_claims

        # Save after every successful example.
        with OUTPUT_FILE.open("w", encoding="utf-8") as file:
            json.dump(predictions, file, indent=4, ensure_ascii=False)

        # Remove an earlier error if this example now succeeds.
        errors.pop(example_id, None)

        print("Extracted claims:", len(extracted_claims))
        for claim in extracted_claims:
            print("-", claim)

    except Exception as error:
        errors[example_id] = str(error)
        print(f"Error processing {example_id}: {error}")

    # Save errors after every example.
    with ERROR_FILE.open("w", encoding="utf-8") as file:
        json.dump(errors, file, indent=4, ensure_ascii=False)

print("\n--- GENERATION SUMMARY ---")
print("Examples in dataset:", len(REFERENCE_DATASET))
print("Successfully processed:", len(predictions))
print("Failed examples:", len(errors))
print("Predictions saved to:", OUTPUT_FILE)
print("Errors saved to:", ERROR_FILE)
