
from schemas.claim_schema import VeriFactOutputSchema


class OutputBuilder:
    """
    Combines generation, sampling and claim extraction results
    into one validated VeriFact AI output.
    """

    def build_output(
        self,
        question: str,
        original_result: dict,
        sample_result: dict,
        claim_result: dict
    ) -> VeriFactOutputSchema:
        """
        Build and validate the complete project output.
        """

        # Prepare the claim summary
        claim_summary = {
            "sentence_count": claim_result["sentence_count"],
            "claim_count": claim_result["claim_count"],
            "valid_claim_count": claim_result["valid_claim_count"],
            "invalid_claim_count": claim_result["invalid_claim_count"]
        }

        # Combine the results from all modules
        output_data = {
            "question": question,
            "original_answer": original_result["answer"],
            "model": original_result["model"],
            "samples": sample_result["samples"],
            "claims": claim_result["claims"],
            "claim_summary": claim_summary
        }

        # Validate the combined output using Pydantic
        validated_output = VeriFactOutputSchema.model_validate(
            output_data
        )

        return validated_output
