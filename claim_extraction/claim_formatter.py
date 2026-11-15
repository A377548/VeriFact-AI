
from claim_extraction.entity_extractor import EntityExtractor


class ClaimFormatter:
    """
    Assigns unique IDs to factual claims and attaches
    their extracted named entities.
    """

    def __init__(self):
        self.entity_extractor = EntityExtractor()

    def format_claims(self, claims: list) -> list:
        """
        Convert a list of factual claims into structured records.
        """

        # Validate input
        if not isinstance(claims, list):
            raise ValueError("Claims must be provided as a list.")

        formatted_claims = []

        for index, claim in enumerate(claims, start=1):

            # Validate each claim
            if not isinstance(claim, str) or not claim.strip():
                raise ValueError(
                    f"Claim at position {index} must be a non-empty string."
                )

            cleaned_claim = claim.strip()

            # Extract named entities from this claim
            entities = self.entity_extractor.extract_entities(
                cleaned_claim
            )

            # Assign a unique claim ID
            claim_id = f"C{index:03d}"

            # Create the structured claim record
            claim_record = {
                "claim_id": claim_id,
                "claim": cleaned_claim,
                "entities": entities
            }

            formatted_claims.append(claim_record)

        return formatted_claims
