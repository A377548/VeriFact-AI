
from generation.llm_client import GeminiClient, MODEL_NAME

print("Testing Gemini API...")
print("Model:", MODEL_NAME)

try:
    client = GeminiClient()
    response = client.generate_text(
        "In one sentence, explain what penicillin is."
    )

    print("\nGemini API is working!")
    print("Response:", response)

except Exception as error:
    print("\nGemini API test failed.")
    print("Reason:", error)
