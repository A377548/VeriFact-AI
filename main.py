
from generation.response_generator import ResponseGenerator
from generation.sample_generator import SampleGenerator
from claim_extraction.claim_pipeline import ClaimExtractionPipeline
from schemas.output_builder import OutputBuilder


def main():
    """
    Main entry point for VeriFact AI.

    Generates an original answer, independent samples,
    extracts factual claims and builds standardized output.
    """

    print("\n===================================")
    print("       Welcome to VeriFact AI")
    print("===================================")

    question = input("\nEnter your question: ").strip()

    try:
        if not question:
            raise ValueError("Question cannot be empty.")

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
            print("Valid:", claim["is_valid"])

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

        # Step 4: Build standardized output
        print("\nBuilding standardized VeriFact AI output...")

        output_builder = OutputBuilder()

        final_output = output_builder.build_output(
            question=question,
            original_result=original_result,
            sample_result=sample_result,
            claim_result=claim_result
        )

        # Step 5: Display summary
        print("\n--- VeriFact AI Summary ---")

        print("Question:", final_output.question)
        print("Model:", final_output.model)

        print(
            "Sentence count:",
            final_output.claim_summary.sentence_count
        )

        print(
            "Factual claim count:",
            final_output.claim_summary.claim_count
        )

        print(
            "Valid claims:",
            final_output.claim_summary.valid_claim_count
        )

        print(
            "Invalid claims:",
            final_output.claim_summary.invalid_claim_count
        )

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

        # Step 6: Display standardized JSON
        print("\n--- Standardized VeriFact AI JSON ---")

        print(final_output.model_dump_json(indent=4))

    except ValueError as error:
        print("\nInput Error:", error)

    except RuntimeError as error:
        print("\nProcessing Error:", error)


if __name__ == "__main__":
    main()
