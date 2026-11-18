
import sys
import os

PROJECT_ROOT = r"G:\College\Text Analytics\VeriFact-AI"
sys.path.insert(0, PROJECT_ROOT)

from hallucination_detection.nli_detector import NLIDetector

print("Loading NLI model...")
detector = NLIDetector()

claim = "Alexander Fleming discovered penicillin."

samples = [
    "Alexander Fleming discovered penicillin in 1928.",
    "Alexander Fleming did not discover penicillin.",
    "The Earth revolves around the Sun.",
    "Alexander Fleming was born in Scotland.",
    "Marie Curie discovered radium."
]

expected = [
    "entailment",
    "contradiction",
    "neutral",
    "neutral",
    "neutral"
]

print("\nRunning expanded NLI evaluation...")

result = detector.check(claim, samples)

correct = 0

print("\n========== EXPANDED NLI RESULTS ==========")

for i, prediction in enumerate(result["results"]):

    predicted = prediction["predicted_relation"].lower()

    print("\nTest case:", i + 1)
    print("Sample:", prediction["sample"])
    print("Expected:", expected[i])
    print("Predicted:", predicted)

    print("Entailment:", prediction["entailment"])
    print("Contradiction:", prediction["contradiction"])
    print("Neutral:", prediction["neutral"])

    if predicted == expected[i]:
        print("Result: CORRECT")
        correct += 1
    else:
        print("Result: INCORRECT")

print("\n========== SUMMARY ==========")
print("Correct:", correct, "/", len(expected))
print("Incorrect:", len(expected) - correct)
print("Diagnostic accuracy:", round(correct / len(expected) * 100, 2), "%")

print("\nExpanded NLI evaluation completed!")
