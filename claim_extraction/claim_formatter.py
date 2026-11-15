
from claim_extraction.entity_extractor import EntityExtractor


class ClaimFormatter:
    """
    Assigns unique IDs to factual claims and attaches
    named entities and original source sentences.
    """

    def __init__(self):
        self.entity_extractor = EntityExtractor()

    def format_claims(
        self,
        claims: list,
        sentences: list
    ) -> list:
        """
        Convert extracted claims into structured records.
        """

        if not isinstance(claims, list):
            raise ValueError("Claims must be provided as a list.")

        if not isinstance(sentences, list):
            raise ValueError("Sentences must be provided as a list.")

        formatted_claims = []

        for index, item in enumerate(claims, start=1):

            if not isinstance(item, dict):
                raise ValueError(
                    f"Claim at position {index} must be a dictionary."
                )

            claim = item.get("claim")
            source_indices = item.get("source_sentence_indices")

            if not isinstance(claim, str) or not claim.strip():
                raise ValueError(
                    f"Claim at position {index} must be a non-empty string."
                )

            if not isinstance(source_indices, list) or not source_indices:
                raise ValueError(
                    f"Claim at position {index} must have source sentence indices."
                )

            # Validate sentence references
            if not all(
                isinstance(source_index, int)
                and not isinstance(source_index, bool)
                and 1 <= source_index <= len(sentences)
                for source_index in source_indices
            ):
                raise ValueError(
                    f"Claim at position {index} has invalid source indices."
                )

            cleaned_claim = claim.strip()

            # Retrieve original source sentence text
            source_sentences = [
                sentences[source_index - 1]
                for source_index in dict.fromkeys(source_indices)
            ]

            # Extract named entities
            entities = self.entity_extractor.extract_entities(
                cleaned_claim
            )

            claim_record = {
                "claim_id": f"C{index:03d}",
                "claim": cleaned_claim,
                "source_sentence_indices": list(
                    dict.fromkeys(source_indices)
                ),
                "source_sentences": source_sentences,
                "entities": entities
            }

            formatted_claims.append(claim_record)

        return formatted_claims
