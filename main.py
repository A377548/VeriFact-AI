
from generation.response_generator import ResponseGenerator
from generation.sample_generator import SampleGenerator


def main():
    """
    Main entry point for VeriFact AI.
    Generates an original answer and multiple independent samples.
    """

    print("\n===================================")
    print("       Welcome to VeriFact AI")
    print("===================================")

    question = input("\nEnter your question: ")

    try:
        # Generate the original answer
        print("\nGenerating original answer...")

        response_generator = ResponseGenerator()
        original_result = (
            response_generator.generate_original_response(question)
        )

        print("\n--- Original Answer ---")
        print(original_result["answer"])

        # Generate independent alternative answers
        print("\nGenerating independent samples...")

        sample_generator = SampleGenerator()
        sample_result = sample_generator.generate_samples(
            question,
            number_of_samples=3
        )

        print("\n--- Independent Samples ---")

        for sample in sample_result["samples"]:
            print(f"\nSample {sample['sample_id']}:")
            print(sample["answer"])

        # Display generation details
        print("\n--- Generation Summary ---")
        print("Question:", question.strip())
        print("Model:", original_result["model"])
        print("Requested samples:", sample_result["requested_samples"])
        print("Successful samples:", sample_result["sample_count"])
        print("Generation status:", sample_result["status"])

        # Display any sample-generation errors
        if sample_result["errors"]:
            print("\n--- Sample Generation Errors ---")

            for error in sample_result["errors"]:
                print(
                    f"Sample {error['sample_id']} failed: "
                    f"{error['error']}"
                )

    except ValueError as error:
        print("\nInput Error:", error)

    except RuntimeError as error:
        print("\nGeneration Error:", error)


if __name__ == "__main__":
    main()
