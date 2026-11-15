
"""
Small manually annotated dataset for evaluating
VeriFact AI claim extraction.
"""

REFERENCE_DATASET = [
    {
        "example_id": "E001",
        "answer": (
            "Alexander Fleming discovered penicillin in 1928. "
            "He made the discovery at St. Mary's Hospital in London."
        ),
        "reference_claims": [
            "Alexander Fleming discovered penicillin.",
            "Penicillin was discovered in 1928.",
            "Alexander Fleming made the discovery at St. Mary's Hospital.",
            "St. Mary's Hospital is located in London."
        ]
    },
    {
        "example_id": "E002",
        "answer": (
            "Marie Curie discovered polonium and radium. "
            "She received the Nobel Prize in Physics in 1903."
        ),
        "reference_claims": [
            "Marie Curie discovered polonium.",
            "Marie Curie discovered radium.",
            "Marie Curie received the Nobel Prize in Physics in 1903."
        ]
    },
    {
        "example_id": "E003",
        "answer": (
            "The Eiffel Tower is located in Paris. "
            "It was completed in 1889."
        ),
        "reference_claims": [
            "The Eiffel Tower is located in Paris.",
            "The Eiffel Tower was completed in 1889."
        ]
    }
]
