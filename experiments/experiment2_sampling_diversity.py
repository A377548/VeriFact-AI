
import json
import re
from itertools import combinations
from pathlib import Path


def tokenize(text):
    """Convert an answer into a set of lowercase words."""
    return set(re.findall(r"\b[a-z0-9]+\b", text.lower()))


def calculate_jaccard_similarity(text1, text2):
    """Calculate lexical overlap between two answers."""
    words1 = tokenize(text1)
    words2 = tokenize(text2)

    union = words1 | words2

    if not union:
        return 0.0

    intersection = words1 & words2

    return round(len(intersection) / len(union), 4)


def main():
    input_path = Path("data/experiment1_samples.json")

    with open(input_path, "r", encoding="utf-8") as file:
        experiment_data = json.load(file)

    samples = experiment_data["successful_samples"]

    if len(samples) < 2:
        raise ValueError("At least two successful samples are required.")

    print("=" * 55)
    print("EXPERIMENT 2: SAMPLING DIVERSITY")
    print("=" * 55)

    pairwise_results = []

    for sample1, sample2 in combinations(samples, 2):
        similarity = calculate_jaccard_similarity(
            sample1["answer"],
            sample2["answer"]
        )

        diversity = round(1 - similarity, 4)

        result = {
            "sample_1": sample1["sample_id"],
            "sample_2": sample2["sample_id"],
            "jaccard_similarity": similarity,
            "lexical_diversity": diversity
        }

        pairwise_results.append(result)

        print(
            f"\nSample {sample1['sample_id']} vs "
            f"Sample {sample2['sample_id']}"
        )
        print("Jaccard similarity:", similarity)
        print("Lexical diversity:", diversity)

    average_similarity = round(
        sum(item["jaccard_similarity"] for item in pairwise_results)
        / len(pairwise_results),
        4
    )

    average_diversity = round(1 - average_similarity, 4)

    output = {
        "experiment": "Sampling Diversity",
        "question": experiment_data["question"],
        "model": experiment_data["model"],
        "successful_sample_count": len(samples),
        "metric": "Word-set Jaccard similarity",
        "pairwise_results": pairwise_results,
        "average_similarity": average_similarity,
        "average_lexical_diversity": average_diversity,
        "interpretation_note": (
            "Lexical overlap measures word-set similarity, "
            "not semantic similarity or factual correctness."
        )
    }

    output_path = Path("data/experiment2_diversity.json")

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)

    print("\n" + "=" * 55)
    print("FINAL RESULTS")
    print("=" * 55)
    print("Number of responses:", len(samples))
    print("Average lexical similarity:", average_similarity)
    print("Average lexical diversity:", average_diversity)
    print("\nResults saved to:", output_path)


if __name__ == "__main__":
    main()
