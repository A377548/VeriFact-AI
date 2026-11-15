
import json
import re

from generation.llm_client import GeminiClient


class AtomicClaimExtractor:
    """
    Extracts atomic factual claims and tracks
    the original sentences supporting each claim.
    """

    def __init__(self):
        self.gemini = GeminiClient()

    def extract_claims(self, answer: str) -> list:
        """
        Extract atomic factual claims with source sentence indices.
        Sentence indices start at 1.
        """

        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty.")

        # Split the answer into numbered source sentences
        from claim_extraction.sentence_splitter import SentenceSplitter

        sentences = SentenceSplitter().split_sentences(answer)

        numbered_sentences = "\n".join(
            f"{index}. {sentence}"
            for index, sentence in enumerate(sentences, start=1)
        )

        prompt = f"""
You are a factual claim extraction system.

Extract atomic, independently verifiable factual claims
from the numbered sentences below.


Instructions:
1. Split complex sentences into atomic, independently verifiable factual claims.
2. Preserve the original meaning of every claim.
3. Resolve pronouns such as "he", "she", "it", "they", "this" and "that" when their references are clear from the surrounding sentences.
4. Replace resolved pronouns with the actual person, organization, place, event or object they refer to.
5. Resolve references such as "the discovery", "the invention", "this event" and "the organization" when their meaning is clear from the context.
6. Do not guess the identity of an unclear pronoun or reference.
7. Do not introduce facts that are not present in the original answer.
8. Keep each claim concise, factual and independently understandable.
9. Exclude opinions, speculation and non-factual filler.
10. For every claim, identify the original sentence numbers that provide its factual information or necessary context.
11. Include multiple sentence numbers when a claim depends on information from more than one sentence.
12. Use one-based sentence numbering.
13. Do not include unrelated sentences in the source references.
14. Return ONLY a valid JSON array.
15. Each array item must have:
    - "claim": a factual claim as a string
    - "source_sentence_indices": an array of sentence numbers
16. If there are no factual claims, return [].


Example output:
[
    {{
        "claim": "Alexander Fleming discovered penicillin.",
        "source_sentence_indices": [1]
    }},
    {{
        "claim": "Alexander Fleming made the discovery at St. Mary's Hospital.",
        "source_sentence_indices": [1, 2]
    }}
]

Numbered original sentences:
{numbered_sentences}
"""

        response = self.gemini.generate_text(prompt)

        # Remove Markdown code fences if present
        cleaned_response = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            response.strip(),
            flags=re.IGNORECASE
        ).strip()

        try:
            claims = json.loads(cleaned_response)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Gemini returned invalid JSON during claim extraction."
            ) from exc

        if not isinstance(claims, list):
            raise RuntimeError(
                "Claim extraction must return a JSON array."
            )

        validated_claims = []
        seen_claims = set()

        for index, item in enumerate(claims, start=1):

            if not isinstance(item, dict):
                raise RuntimeError(
                    f"Claim record {index} must be a JSON object."
                )

            claim = item.get("claim")
            source_indices = item.get("source_sentence_indices")

            if not isinstance(claim, str) or not claim.strip():
                raise RuntimeError(
                    f"Claim record {index} has an invalid claim."
                )

            if not isinstance(source_indices, list) or not source_indices:
                raise RuntimeError(
                    f"Claim record {index} must have source sentence indices."
                )

            if not all(
                isinstance(source_index, int)
                and not isinstance(source_index, bool)
                and 1 <= source_index <= len(sentences)
                for source_index in source_indices
            ):
                raise RuntimeError(
                    f"Claim record {index} contains invalid sentence indices."
                )

            # Remove duplicate indices while preserving order
            unique_indices = list(dict.fromkeys(source_indices))

            cleaned_claim = claim.strip()

            if cleaned_claim.casefold() not in seen_claims:
                validated_claims.append({
                    "claim": cleaned_claim,
                    "source_sentence_indices": unique_indices
                })

                seen_claims.add(cleaned_claim.casefold())

        return validated_claims
