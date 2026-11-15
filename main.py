
from generation.response_generator import ResponseGenerator
from generation.sample_generator import SampleGenerator
from claim_extraction.claim_pipeline import ClaimExtractionPipeline


def main():
    """
    Main entry point for VeriFact AI.
    Generates an original answer, independent samples,
    and structured factual claims.
    """

    print("\n===================================")
    print("       Welcome to VeriFact AI")
    print("===================================")

    question = input("\nEnter your question: ")

    try:
        # Step 1: Generate the original answer
        print("\nGenerating original answer...")

        response_generator = ResponseGenerator()
        original_result = (
            response_generator.generate_original_response(question)
        )

        print("\n--- Original Answer ---")
        print(original_result["answer"])

        # Step 2: Extract structured factual claims
        print("\nExtracting factual claims...")

        claim_pipeline = ClaimExtractionPipeline()
        claim_result = claim_pipeline.process_answer(
            original_result["answer"]
        )

        print("\n--- Sentence Segmentation ---")

        for sentence in claim_result["sentences"]:
            print("-", sentence)

        print("\n--- Structured Factual Claims ---")

        for claim in claim_result["claims"]:
            print(f"\nClaim ID: {claim['claim_id']}")
            print("Claim:", claim["claim"])

            print("Entities:")

            if claim["entities"]:
                for entity in claim["entities"]:
                    print(
                        f"  - {entity['text']} "
                        f"({entity['label']})"
                    )
            else:
                print("  - No named entities identified")

        # Step 3: Generate independent samples
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

        # Step 4: Display summary
        print("\n--- VeriFact AI Summary ---")
        print("Question:", question.strip())
        print("Model:", original_result["model"])
        print("Sentence count:", claim_result["sentence_count"])
        print("Factual claim count:", claim_result["claim_count"])
        print("Requested samples:", sample_result["requested_samples"])
        print("Successful samples:", sample_result["sample_count"])
        print("Generation status:", sample_result["status"])

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
        print("\nProcessing Error:", error)


if __name__ == "__main__":
    main()
