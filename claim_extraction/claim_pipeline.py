
from claim_extraction.sentence_splitter import SentenceSplitter
from claim_extraction.atomic_claim_extractor import AtomicClaimExtractor
from claim_extraction.claim_formatter import ClaimFormatter
from claim_extraction.claim_validator import ClaimValidator


class ClaimExtractionPipeline:
    """
    Coordinates sentence segmentation, atomic claim extraction,
    entity extraction, source traceability and claim validation.
    """

    def __init__(self):
        self.sentence_splitter = SentenceSplitter()
        self.claim_extractor = AtomicClaimExtractor()
        self.claim_formatter = ClaimFormatter()
        self.claim_validator = ClaimValidator()

    def process_answer(self, answer: str) -> dict:
        """
        Process an LLM-generated answer and return
        structured claims with traceability and quality results.
        """

        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty.")

        # Step 1: Split the original answer into sentences
        sentences = self.sentence_splitter.split_sentences(answer)

        # Step 2: Extract atomic factual claims
        extracted_claims = self.claim_extractor.extract_claims(answer)

        # Step 3: Format claims with IDs, entities and source sentences
        formatted_claims = self.claim_formatter.format_claims(
            extracted_claims,
            sentences
        )

        # Step 4: Validate claim quality
        validation_result = self.claim_validator.validate_claims(
            formatted_claims,
            len(sentences)
        )

        return {
            "original_answer": answer.strip(),
            "sentences": sentences,
            "sentence_count": len(sentences),
            "claims": validation_result["claims"],
            "claim_count": len(formatted_claims),
            "valid_claim_count": validation_result["valid_claims"],
            "invalid_claim_count": validation_result["invalid_claims"],
            "validation_summary": validation_result
        }
