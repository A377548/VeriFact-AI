
import spacy


class EntityExtractor:
    """
    Identifies named entities in factual claims.
    """

    def __init__(self):
        # Load the English NLP model
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text: str) -> list:
        """
        Extract named entities from the given text.
        """

        # Validate input
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        # Process text using spaCy
        doc = self.nlp(text.strip())

        entities = []

        # Extract recognized named entities
        for entity in doc.ents:
            entities.append({
                "text": entity.text,
                "label": entity.label_,
                "description": spacy.explain(entity.label_)
            })

        return entities
