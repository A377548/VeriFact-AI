
from unittest.mock import patch

from generation.sample_generator import SampleGenerator


def test_sample_generator_handles_partial_failure():
    calls = []

    def fake_generate(prompt):
        calls.append(len(calls) + 1)

        # Simulate failure on the second request
        if len(calls) == 2:
            raise RuntimeError("Simulated API failure")

        return f"Simulated answer {len(calls)}"

    # Mock GeminiClient before SampleGenerator is initialized
    with patch("generation.sample_generator.GeminiClient") as mock_client:
        mock_client.return_value.generate_text.side_effect = fake_generate

        generator = SampleGenerator()

        result = generator.generate_samples("Test question", 3)

    # Verify expected behavior
    assert result["sample_count"] == 2
    assert result["requested_samples"] == 3
    assert result["status"] == "partial"
    assert len(result["errors"]) == 1
    assert result["samples"][0]["sample_id"] == 1
    assert result["samples"][1]["sample_id"] == 3
