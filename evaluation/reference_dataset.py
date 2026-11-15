
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
    },
        {
        "example_id": "E004",
        "answer": (
            "Barack Obama was the 44th President of the United States. "
            "He served as president from 2009 to 2017. "
            "He was born in Honolulu, Hawaii."
        ),
        "reference_claims": [
            "Barack Obama was the 44th President of the United States.",
            "Barack Obama served as president from 2009 to 2017.",
            "Barack Obama was born in Honolulu, Hawaii."
        ]
    },
    {
        "example_id": "E005",
        "answer": (
            "Water freezes at 0 degrees Celsius under standard atmospheric pressure. "
            "Water boils at 100 degrees Celsius under standard atmospheric pressure."
        ),
        "reference_claims": [
            "Water freezes at 0 degrees Celsius under standard atmospheric pressure.",
            "Water boils at 100 degrees Celsius under standard atmospheric pressure."
        ]
    },
    {
        "example_id": "E006",
        "answer": (
            "William Shakespeare wrote Hamlet. "
            "Hamlet is a tragedy. "
            "The play is set in Denmark."
        ),
        "reference_claims": [
            "William Shakespeare wrote Hamlet.",
            "Hamlet is a tragedy.",
            "Hamlet is set in Denmark."
        ]
    },
    {
        "example_id": "E007",
        "answer": (
            "Mars is the fourth planet from the Sun. "
            "Mars has two natural moons named Phobos and Deimos."
        ),
        "reference_claims": [
            "Mars is the fourth planet from the Sun.",
            "Mars has two natural moons.",
            "The two moons of Mars are named Phobos and Deimos."
        ]
    },
    {
        "example_id": "E008",
        "answer": (
            "Python is a high-level programming language. "
            "Guido van Rossum created Python. "
            "Python was first released in 1991."
        ),
        "reference_claims": [
            "Python is a high-level programming language.",
            "Guido van Rossum created Python.",
            "Python was first released in 1991."
        ]
    }
    
]
