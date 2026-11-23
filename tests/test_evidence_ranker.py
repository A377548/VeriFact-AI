
import unittest

from evidence_retrieval.evidence_ranker import EvidenceRanker


class TestEvidenceRanker(unittest.TestCase):

    def test_relevant_evidence_ranked_first(self):
        evidence = [
            {
                "title": "Moon",
                "text": "The Moon orbits the Earth."
            },
            {
                "title": "Earth",
                "text": "Earth revolves around the Sun."
            }
        ]

        ranked = EvidenceRanker().rank(
            "Earth revolves around the Sun",
            evidence,
            top_k=2
        )

        self.assertEqual(ranked[0]["title"], "Earth")

    def test_minimum_relevance_filter(self):
        evidence = [
            {
                "title": "Relevant",
                "text": "Earth revolves around the Sun."
            },
            {
                "title": "Irrelevant",
                "text": "Chocolate cake contains sugar and flour."
            }
        ]

        ranked = EvidenceRanker(
            min_relevance=0.5
        ).rank(
            "Earth revolves around the Sun",
            evidence,
            top_k=5
        )

        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0]["title"], "Relevant")

    def test_duplicate_passages_removed(self):
        evidence = [
            {
                "title": "Earth",
                "text": "Earth revolves around the Sun."
            },
            {
                "title": "Earth Copy",
                "text": "EARTH REVOLVES AROUND THE SUN!"
            }
        ]

        ranked = EvidenceRanker().rank(
            "Earth revolves around the Sun",
            evidence,
            top_k=5
        )

        self.assertEqual(len(ranked), 1)

    def test_source_diversity(self):
        evidence = [
            {
                "title": "Article A",
                "url": "https://example.com/a",
                "text": "Earth revolves around the Sun every year."
            },
            {
                "title": "Article A Copy",
                "url": "https://example.com/a",
                "text": "Earth revolves around the Sun and completes an orbit."
            },
            {
                "title": "Article B",
                "url": "https://example.com/b",
                "text": "Earth revolves around the Sun in an annual orbit."
            }
        ]

        ranked = EvidenceRanker(
            max_per_source=1
        ).rank(
            "Earth revolves around the Sun",
            evidence,
            top_k=3
        )

        urls = [item["url"] for item in ranked]

        self.assertEqual(len(urls), len(set(urls)))

    def test_empty_evidence(self):
        ranked = EvidenceRanker().rank(
            "Earth revolves around the Sun",
            [],
            top_k=3
        )

        self.assertEqual(ranked, [])

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            EvidenceRanker(min_relevance=1.5)


if __name__ == "__main__":
    unittest.main()
