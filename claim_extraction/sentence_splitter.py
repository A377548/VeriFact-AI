
import spacy


class SentenceSplitter:
    """
    Splits an LLM-generated answer into individual sentences.
    """

    def __init__(self):
        # Load the English language model
        self.nlp = spacy.load("en_core_web_sm")

    def split_sentences(self, text: str) -> list:
        """
        Split the given text into individual sentences.
        """

        # Validate the input
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        # Process the text using spaCy
        doc = self.nlp(text.strip())

        # Extract individual sentences
        sentences = [
            sentence.text.strip()
            for sentence in doc.sents
            if sentence.text.strip()
        ]

        return sentences
