
from explanation.adaptive_verifier import AdaptiveEvidenceVerifier

verifier = AdaptiveEvidenceVerifier()

claims = [
    ("C01", "Mars is the fourth planet from the Sun."),
    ("C05", "The Sun revolves around the Earth."),
    ("C09", "The universe contains exactly 17 planets."),
    ("C10", "Every star in the universe has at least one planet.")
]

for claim_id, claim in claims:
    print("\n" + "=" * 70)
    print("CLAIM:", claim_id, "-", claim)

    result = verifier.verify(claim_id, claim)

    print("VERDICT:", result["final_relation"])
    print("RELATION COUNTS:", result["relation_counts"])

    for index, evidence in enumerate(result.get("evidence", []), 1):
        print(f"\nEvidence {index}:")

        for key, value in evidence.items():
            if key == "text" and isinstance(value, str):
                value = value[:400] + "..."
            print(f"  {key}: {value}")
