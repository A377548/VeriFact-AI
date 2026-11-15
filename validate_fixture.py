
import json

from schemas.claim_schema import VeriFactOutputSchema

with open("data/sample_verifact_output.json", "r", encoding="utf-8") as file:
    data = json.load(file)

validated_output = VeriFactOutputSchema.model_validate(data)

print("\nPydantic validation passed!")
print("Question:", validated_output.question)
print("Schema version:", validated_output.schema_version)
print("Number of samples:", len(validated_output.samples))
print("Number of claims:", len(validated_output.claims))
print("Valid claims:", validated_output.claim_summary.valid_claim_count)
