
import sys
from pathlib import Path

# Find the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add project root BEFORE importing the package
sys.path.insert(0, str(PROJECT_ROOT))

print("Project root:", PROJECT_ROOT)
print("Python path:", sys.path[0])

# Verify package folder
package_path = PROJECT_ROOT / "hallucination_detection"

if not package_path.exists():
    raise FileNotFoundError(
        f"hallucination_detection folder not found: {package_path}"
    )

print("Detection package found!")

# Import after setting Python path
from hallucination_detection.detection_pipeline import (
    HallucinationDetectionPipeline
)

print("\nLoading detection models...")

pipeline = HallucinationDetectionPipeline()

input_data = {
    "project": "VeriFact AI",
    "schema_version": "1.0",
    "question": "Who discovered penicillin?",
    "original_answer": "Alexander Fleming discovered penicillin in 1928.",
    "model": "gemini-3.8-flash",
    "samples": [
        {
            "sample_id": 1,
            "answer": "Alexander Fleming discovered penicillin in 1928."
        },
        {
            "sample_id": 2,
            "answer": "Marie Curie discovered radium."
        },
        {
            "sample_id": 3,
            "answer": "Penicillin was discovered in the twentieth century."
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

print("\nRunning real hallucination detection...")

result = pipeline.process(input_data)

print("\n========== VERIFACT AI RESULTS ==========")

print("Question:", result["question"])
print("Overall risk:", result["overall_risk_score"])

for item in result["results"]:
    print("\n------------------------------------")
    print("Claim ID:", item["claim_id"])
    print("Claim:", item["claim"])

    print("SelfCheck:", item["selfcheck"])
    print("BERTScore:", item["bertscore"])
    print("Combined score:", item["combined_score"])

    print("\nNLI predictions:")

    for prediction in item["nli"]["results"]:
        print(
            prediction["predicted_relation"],
            "-",
            prediction["sample"]
        )

print("\nReal pipeline execution completed!")
