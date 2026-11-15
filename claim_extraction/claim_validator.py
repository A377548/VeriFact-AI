
class ClaimValidator:
    """
    Checks the quality of extracted factual claims.

    Identifies empty claims, duplicates, vague references,
    and missing or invalid source references.
    """

    VAGUE_STARTERS = (
        "it ",
        "this ",
        "that ",
        "they ",
        "he ",
        "she ",
        "these ",
        "those "
    )

    def validate_claims(self, claims: list, sentence_count: int) -> dict:

        if not isinstance(claims, list):
            raise ValueError("Claims must be provided as a list.")

        if (
            isinstance(sentence_count, bool)
            or not isinstance(sentence_count, int)
            or sentence_count < 0
        ):
            raise ValueError("Sentence count must be a non-negative integer.")

        validated = []
        seen = set()

        for claim in claims:

            issues = []

            if not isinstance(claim, dict):
                validated.append({
                    "claim": str(claim),
                    "is_valid": False,
                    "issues": ["Claim must be a dictionary."]
                })
                continue

            text = claim.get("claim")

            if not isinstance(text, str) or not text.strip():
                issues.append("Empty or invalid claim.")
                text = ""

            cleaned_text = text.strip()

            if cleaned_text:
                normalized = cleaned_text.casefold()

                if normalized in seen:
                    issues.append("Duplicate claim.")
                else:
                    seen.add(normalized)

                if cleaned_text.casefold().startswith(
                    self.VAGUE_STARTERS
                ):
                    issues.append(
                        "Claim may contain an unresolved reference."
                    )

            source_indices = claim.get("source_sentence_indices")

            if not isinstance(source_indices, list) or not source_indices:
                issues.append("Missing source sentence references.")

            elif not all(
                isinstance(index, int)
                and not isinstance(index, bool)
                and 1 <= index <= sentence_count
                for index in source_indices
            ):
                issues.append("Invalid source sentence references.")

            validated.append({
                **claim,
                "is_valid": len(issues) == 0,
                "issues": issues
            })

        return {
            "total_claims": len(claims),
            "valid_claims": sum(
                item["is_valid"] for item in validated
            ),
            "invalid_claims": sum(
                not item["is_valid"] for item in validated
            ),
            "claims": validated
        }
