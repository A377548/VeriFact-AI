from generation.response_generator import ResponseGenerator


def main():
    """
    Main entry point for VeriFact AI.
    """

    print("\n===================================")
    print("       Welcome to VeriFact AI")
    print("===================================")

    question = input("\nEnter your question: ")

    try:
        generator = ResponseGenerator()

        result = generator.generate_original_response(question)

        print("\n--- Generated Answer ---")
        print(result["answer"])

        print("\n--- Generation Details ---")
        print("Question:", result["question"])
        print("Model:", result["model"])

    except ValueError as error:
        print("\nInput Error:", error)

    except RuntimeError as error:
        print("\nGeneration Error:", error)


if __name__ == "__main__":
    main()