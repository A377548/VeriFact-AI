
import json
import time
from pathlib import Path

from generation.sample_generator import SampleGenerator


def main():
    question = "Who discovered penicillin and when?"

    print("=" * 50)
    print("EXPERIMENT 1: EFFECT OF SAMPLE COUNT")
    print("=" * 50)

    generator = SampleGenerator()

    start_time = time.perf_counter()

    # Generate five independent responses in one run
    result = generator.generate_samples(
        question=question,
        number_of_samples=5
    )

    end_time = time.perf_counter()
    total_time = round(end_time - start_time, 2)

    # Compare the first 1, first 3 and all 5 successful samples
    sample_counts = [1, 3, 5]

    print("\n--- EXPERIMENT RESULTS ---")

    for count in sample_counts:
        available = min(count, result["sample_count"])

        print(f"\nRequested sample count: {count}")
        print(f"Available samples: {available}")

        if available < count:
            print("Status: Insufficient successful samples")
        else:
            print("Status: Completed")

    print("\nTotal successful samples:", result["sample_count"])
    print("Total failed requests:", len(result["errors"]))
    print("Total generation time:", total_time, "seconds")
    print("Generation status:", result["status"])

    # Preserve all results for analysis and the project report
    output = {
        "experiment": "Effect of Sample Count",
        "question": question,
        "model": result["model"],
        "requested_sample_counts": sample_counts,
        "successful_samples": result["samples"],
        "sample_count": result["sample_count"],
        "errors": result["errors"],
        "generation_status": result["status"],
        "total_generation_time_seconds": total_time
    }

    output_path = Path("data/experiment1_samples.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)

    print("\nExperiment results saved to:", output_path)


if __name__ == "__main__":
    main()
