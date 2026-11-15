
import json
import re

from generation.llm_client import GeminiClient


class AtomicClaimExtractor:
    """
    Extracts independently verifiable factual claims
    from an LLM-generated answer.
    """

    def __init__(self):
        self.gemini = GeminiClient()

    def extract_claims(self, answer: str) -> list:
        """
        Extract atomic factual claims from the given answer.
        """

        # Validate input
        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty.")

        prompt = f"""
You are a factual claim extraction system.

Your task is to extract atomic, independently verifiable
factual claims from the answer provided below.

Instructions:
1. Split complex sentences into smaller factual claims.
2. Each claim should express one independently verifiable fact.
3. Preserve names, dates, places, numbers and relationships.
4. Resolve pronouns when their references are clear.
5. Do not introduce facts that are not stated or clearly
   implied by the original answer.
6. Do not change the meaning of the original statements.
7. Exclude opinions, greetings and non-factual filler.
8. Avoid unnecessary repetition.
9. Keep claims concise and understandable on their own.
10. Return ONLY a valid JSON array of strings.
11. If there are no factual claims, return [].

Example output:
[
    "Alexander Fleming discovered penicillin.",
    "Penicillin was discovered in 1928.",
    "Alexander Fleming made the discovery at St. Mary's Hospital."
]

Original answer:
{answer}
"""

        # Ask Gemini to extract claims
        response = self.gemini.generate_text(prompt)

        # Remove Markdown code fences if Gemini includes them
        cleaned_response = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            response.strip(),
            flags=re.IGNORECASE
        ).strip()

        # Parse the JSON response
        try:
            claims = json.loads(cleaned_response)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Gemini returned an invalid JSON response "
                "during claim extraction."
            ) from exc

        # Validate the response structure
        if not isinstance(claims, list):
            raise RuntimeError(
                "Claim extraction must return a JSON array."
            )

        if not all(
            isinstance(claim, str) and claim.strip()
            for claim in claims
        ):
            raise RuntimeError(
                "Every extracted claim must be a non-empty string."
            )

        # Remove exact duplicate claims while preserving order
        unique_claims = []
        seen_claims = set()

        for claim in claims:
            cleaned_claim = claim.strip()

            if cleaned_claim.casefold() not in seen_claims:
                unique_claims.append(cleaned_claim)
                seen_claims.add(cleaned_claim.casefold())

        return unique_claims
