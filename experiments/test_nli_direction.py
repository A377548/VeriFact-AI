
import sys
import os

# STEP 1: Set the exact project root
PROJECT_ROOT = r"G:\College\Text Analytics\VeriFact-AI"

# STEP 2: Add project root BEFORE importing modules
sys.path.insert(0, PROJECT_ROOT)

print("Project root:", PROJECT_ROOT)
print("Python path configured.")

# STEP 3: Verify detection folder
package_path = os.path.join(
    PROJECT_ROOT,
    "hallucination_detection"
)

if not os.path.isdir(package_path):
    raise FileNotFoundError(
        "Detection folder not found: " + package_path
    )

print("Detection folder found!")

# STEP 4: Import NLI detector
from hallucination_detection.nli_detector import NLIDetector


# STEP 5: Load model
print("\nLoading NLI model...")

detector = NLIDetector()

print("NLI model loaded successfully!")


# STEP 6: Prepare test cases
claim = "Alexander Fleming discovered penicillin."

samples = [
    "Alexander Fleming discovered penicillin in 1928.",
    "Alexander Fleming did not discover penicillin.",
    "The Earth revolves around the Sun.",
    "Marie Curie discovered radium."
]


# STEP 7: Compare original and reversed directions
print("\n========== NLI DIRECTION TEST ==========")

for sample in samples:

    print("\n----------------------------------------")
    print("Sample:", sample)

    # Original direction:
    # Premise = sample
    # Hypothesis = claim
    forward = detector.classifier({
        "text": sample,
        "text_pair": claim
    })

    # Reversed direction:
    # Premise = claim
    # Hypothesis = sample
    reverse = detector.classifier({
        "text": claim,
        "text_pair": sample
    })

    print("\nOriginal direction:")

    for item in forward:
        print(
            item["label"],
            round(item["score"], 4)
        )

    print("\nReversed direction:")

    for item in reverse:
        print(
            item["label"],
            round(item["score"], 4)
        )


print("\n========================================")
print("NLI direction test completed!")
print("========================================")
