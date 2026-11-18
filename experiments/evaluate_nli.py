
import sys
from pathlib import Path
from collections import defaultdict

# Add the project root to Python's import path FIRST.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

print("Project root:", PROJECT_ROOT)
print("Python path:", sys.path[0])

# Import only after setting the project path.
from hallucination_detection.nli_detector import NLIDetector


TEST_CASES = [
    # ENTAILMENT
    {
        "premise": "Alexander Fleming discovered penicillin in 1928.",
        "hypothesis": "Alexander Fleming discovered penicillin.",
        "expected": "entailment"
    },
    {
        "premise": "The Earth revolves around the Sun.",
        "hypothesis": "Earth orbits the Sun.",
        "expected": "entailment"
    },
    {
        "premise": "Water freezes at zero degrees Celsius under standard pressure.",
        "hypothesis": "Water freezes at 0 degrees Celsius under standard pressure.",
        "expected": "entailment"
    },
    {
        "premise": "William Shakespeare wrote the play Hamlet.",
        "hypothesis": "Hamlet was written by William Shakespeare.",
        "expected": "entailment"
    },
    {
        "premise": "The Pacific Ocean is the largest ocean on Earth.",
        "hypothesis": "The Pacific is Earth's largest ocean.",
        "expected": "entailment"
    },

    # CONTRADICTION
    {
        "premise": "Alexander Fleming did not discover penicillin.",
        "hypothesis": "Alexander Fleming discovered penicillin.",
        "expected": "contradiction"
    },
    {
        "premise": "The Earth does not revolve around the Sun.",
        "hypothesis": "The Earth revolves around the Sun.",
        "expected": "contradiction"
    },
    {
        "premise": "Water freezes at 50 degrees Celsius under standard pressure.",
        "hypothesis": "Water freezes at 0 degrees Celsius under standard pressure.",
        "expected": "contradiction"
    },
    {
        "premise": "William Shakespeare did not write Hamlet.",
        "hypothesis": "William Shakespeare wrote Hamlet.",
        "expected": "contradiction"
    },
    {
        "premise": "The Atlantic Ocean is the largest ocean on Earth.",
        "hypothesis": "The Pacific Ocean is the largest ocean on Earth.",
        "expected": "contradiction"
    },

    # NEUTRAL
    {
        "premise": "Marie Curie discovered radium.",
        "hypothesis": "Alexander Fleming discovered penicillin.",
        "expected": "neutral"
    },
    {
        "premise": "The Earth has one natural satellite called the Moon.",
        "hypothesis": "Water freezes at zero degrees Celsius.",
        "expected": "neutral"
    },
    {
        "premise": "William Shakespeare was born in Stratford-upon-Avon.",
        "hypothesis": "The Pacific Ocean is the largest ocean.",
        "expected": "neutral"
    },
    {
        "premise": "The human heart has four chambers.",
        "hypothesis": "Alexander Fleming discovered penicillin.",
        "expected": "neutral"
    },
    {
        "premise": "Mount Everest is located in the Himalayas.",
        "hypothesis": "William Shakespeare wrote Hamlet.",
        "expected": "neutral"
    }
]


def main():
    print("\n========================================")
    print("       VERIFACT AI - NLI EVALUATION")
    print("========================================")

    print("\nLoading NLI model...")
    detector = NLIDetector()

    correct = 0
    total = len(TEST_CASES)
    confusion = defaultdict(int)

    for index, case in enumerate(TEST_CASES, start=1):
        result = detector.check(
            case["hypothesis"],
            [case["premise"]]
        )

        predicted = result["results"][0]["predicted_relation"]
        expected = case["expected"]

        is_correct = predicted == expected

        if is_correct:
            correct += 1

        confusion[(expected, predicted)] += 1

        print(f"\nTest Case {index}")
        print("Premise:", case["premise"])
        print("Hypothesis:", case["hypothesis"])
        print("Expected:", expected)
        print("Predicted:", predicted)
        print("Result:", "CORRECT" if is_correct else "INCORRECT")

    accuracy = (correct / total) * 100

    print("\n========================================")
    print("             FINAL RESULTS")
    print("========================================")

    print(f"Total test cases: {total}")
    print(f"Correct predictions: {correct}")
    print(f"Incorrect predictions: {total - correct}")
    print(f"Accuracy: {accuracy:.2f}%")

    print("\nConfusion Matrix")

    labels = ["entailment", "contradiction", "neutral"]

    print(f"{'Expected / Predicted':<22}", end="")
    for label in labels:
        print(f"{label[:6]:>12}", end="")
    print()

    for expected in labels:
        print(f"{expected:<22}", end="")
        for predicted in labels:
            print(f"{confusion[(expected, predicted)]:>12}", end="")
        print()

    print("\nEvaluation completed.")


if __name__ == "__main__":
    main()
