
from claim_extraction.sentence_splitter import SentenceSplitter
from claim_extraction.atomic_claim_extractor import AtomicClaimExtractor
from claim_extraction.claim_formatter import ClaimFormatter


class ClaimExtractionPipeline:
    """
    Coordinates sentence segmentation, atomic claim extraction,
    entity extraction and structured claim formatting.
    """

    def __init__(self):
        self.sentence_splitter = SentenceSplitter()
        self.claim_extractor = AtomicClaimExtractor()
        self.claim_formatter = ClaimFormatter()

    def process_answer(self, answer: str) -> dict:
        """
        Process an LLM-generated answer and return structured claims.
        """

        # Validate the input
        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty.")

        # Step 1: Split the original answer into sentences
        sentences = self.sentence_splitter.split_sentences(answer)

        # Step 2: Extract atomic claims from the complete answer.
        # Keeping the full context helps resolve pronouns correctly.
        claims = self.claim_extractor.extract_claims(answer)

        # Step 3: Attach entities and assign claim IDs
        formatted_claims = self.claim_formatter.format_claims(claims)

        # Step 4: Return the complete structured result
        return {
            "original_answer": answer.strip(),
            "sentences": sentences,
            "sentence_count": len(sentences),
            "claims": formatted_claims,
            "claim_count": len(formatted_claims)
        }
