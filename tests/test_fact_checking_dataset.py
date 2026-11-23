
from explanation.adaptive_verifier import AdaptiveEvidenceVerifier


# Manually labelled evaluation dataset.
# These are expected labels, not guaranteed model predictions.

DATASET = [
    # SUPPORTED claims
    {
        "id": "C01",
        "claim": "Mars is the fourth planet from the Sun.",
        "expected": "supported"
    },
    {
        "id": "C02",
        "claim": "Water has the chemical formula H2O.",
        "expected": "supported"
    },
    {
        "id": "C03",
        "claim": "The Sun is a star.",
        "expected": "supported"
    },
    {
        "id": "C04",
        "claim": "The Earth revolves around the Sun.",
        "expected": "supported"
    },

    # CONTRADICTED claims
    {
        "id": "C05",
        "claim": "The Sun revolves around the Earth.",
        "expected": "contradicted"
    },
    {
        "id": "C06",
        "claim": "Mars is the fifth planet from the Sun.",
        "expected": "contradicted"
    },
    {
        "id": "C07",
        "claim": "Mercury is the largest planet.",
        "expected": "contradicted"
    },
    {
        "id": "C08",
        "claim": "Water has the chemical formula CO2.",
        "expected": "contradicted"
    },

    # INSUFFICIENT EVIDENCE claims
    {
        "id": "C09",
        "claim": "The universe contains exactly 17 planets.",
        "expected": "insufficient_evidence"
    },
    {
        "id": "C10",
        "claim": "Every star in the universe has at least one planet.",
        "expected": "insufficient_evidence"
    },
    {
        "id": "C11",
        "claim": "A particular undiscovered planet is habitable.",
        "expected": "insufficient_evidence"
    },
    {
        "id": "C12",
        "claim": "There are exactly 500 intelligent civilizations in the universe.",
        "expected": "insufficient_evidence"
    }
]


def calculate_metrics(results):

    total = len(results)

    if total == 0:
        print("\nNo successful evaluations to calculate.")
        return

    correct = sum(
        1 for result in results
        if result["expected"] == result["predicted"]
    )

    accuracy = correct / total

    labels = [
        "supported",
        "contradicted",
        "insufficient_evidence"
    ]

    print("\n" + "=" * 65)
    print("EVALUATION METRICS")
    print("=" * 65)

    print(f"Successfully evaluated: {total}")
    print(f"Correct predictions: {correct}")
    print(f"Incorrect predictions: {total - correct}")
    print(f"Accuracy: {accuracy * 100:.2f}%")

    print("\nCLASS-WISE METRICS")

    for label in labels:

        true_positive = sum(
            1 for r in results
            if r["expected"] == label
            and r["predicted"] == label
        )

        false_positive = sum(
            1 for r in results
            if r["expected"] != label
            and r["predicted"] == label
        )

        false_negative = sum(
            1 for r in results
            if r["expected"] == label
            and r["predicted"] != label
        )

        precision = (
            true_positive / (true_positive + false_positive)
            if true_positive + false_positive else 0
        )

        recall = (
            true_positive / (true_positive + false_negative)
            if true_positive + false_negative else 0
        )

        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall else 0
        )

        print(f"\n{label.upper()}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall:    {recall:.2f}")
        print(f"F1-score:  {f1:.2f}")

    print("\nCONFUSION MATRIX")
    print("Rows = Expected | Columns = Predicted")

    print(
        f"{'Expected':25}"
        f"{'Supported':15}"
        f"{'Contradicted':15}"
        f"{'Insufficient':15}"
    )

    for expected in labels:

        counts = []

        for predicted in labels:
            count = sum(
                1 for r in results
                if r["expected"] == expected
                and r["predicted"] == predicted
            )
            counts.append(count)

        print(
            f"{expected:25}"
            f"{counts[0]:<15}"
            f"{counts[1]:<15}"
            f"{counts[2]:<15}"
        )


def run_evaluation():

    print("=" * 65)
    print("VERIFACT AI - FACT CHECKING EVALUATION")
    print("=" * 65)

    verifier = AdaptiveEvidenceVerifier()

    results = []

    for item in DATASET:

        print("\n" + "-" * 65)
        print(f"Claim ID: {item['id']}")
        print(f"Claim: {item['claim']}")
        print(f"Expected: {item['expected']}")

        try:

            verification = verifier.verify(
                item["id"],
                item["claim"]
            )

            predicted = verification["final_relation"]

            result = {
                "id": item["id"],
                "claim": item["claim"],
                "expected": item["expected"],
                "predicted": predicted
            }

            results.append(result)

            print(f"Predicted: {predicted.upper()}")

            print(
                "Result:",
                "CORRECT" if predicted == item["expected"]
                else "INCORRECT"
            )

            print(
                "Evidence count:",
                verification["evidence_count"]
            )

            print(
                "Adaptive retrieval:",
                verification["expanded"]
            )

            print(
                "Relation counts:",
                verification["relation_counts"]
            )

        except Exception as error:

            print(f"ERROR: {error}")

    calculate_metrics(results)

    print("\nEvaluation completed.")


if __name__ == "__main__":
    run_evaluation()
