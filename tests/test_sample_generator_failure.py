
from generation.sample_generator import SampleGenerator


# Create the sample generator
generator = SampleGenerator()

# Track how many times the simulated API is called
calls = []


# Simulate Gemini responses
def fake_generate(prompt):
    calls.append(len(calls) + 1)

    # Simulate failure on the second request
    if len(calls) == 2:
        raise RuntimeError("Simulated API failure")

    return f"Simulated answer {len(calls)}"


# Replace the real API method with our simulated method
generator.gemini.generate_text = fake_generate


# Generate three samples
result = generator.generate_samples("Test question", 3)

print("\nFinal result:")
print(result)


# Verify the expected behavior
assert result["sample_count"] == 2
assert result["requested_samples"] == 3
assert result["status"] == "partial"
assert len(result["errors"]) == 1
assert result["samples"][0]["sample_id"] == 1
assert result["samples"][1]["sample_id"] == 3

print("\nAll partial-generation tests passed!")
