
import re
import time
import requests


class WikipediaRetriever:
    """
    Retrieves relevant Wikipedia evidence using expanded queries,
    article ranking, paragraph extraction, caching and retries.
    """

    def __init__(self):
        self.api_url = "https://en.wikipedia.org/w/api.php"

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "VeriFactAI/2.0 (academic fact-checking project)"
        })

        self.cache = {}
        self.cache_duration = 600
        self.last_request_time = 0
        self.request_interval = 0.5
        self.max_retries = 3

    def _normalize_text(self, text):
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _get_search_queries(self, claim: str) -> list[str]:
        normalized = self._normalize_text(claim)

        queries = [claim.strip(), normalized]

        # Planet position and order.
        planet_names = [
            "mercury", "venus", "earth", "mars",
            "jupiter", "saturn", "uranus", "neptune"
        ]

        for planet in planet_names:
            if planet in normalized:
                queries.extend([
                    f"{planet} planet distance from Sun",
                    f"{planet} position in Solar System",
                    "order of planets from the Sun"
                ])
                break

        # Earth and Sun.
        if "earth" in normalized and "sun" in normalized:
            queries.extend([
                "Earth orbit heliocentric model",
                "Earth revolves around Sun",
                "heliocentrism",
                "geocentrism"
            ])

        # Water.
        if "water" in normalized:
            queries.extend([
                "chemical formula of water",
                "water chemical composition H2O"
            ])

        # Sun classification.
        if "sun" in normalized and (
            "star" in normalized or "largest" in normalized
        ):
            queries.extend([
                "Sun G-type main-sequence star",
                "stellar classification of the Sun"
            ])

        # Planetary habitability.
        if "habitable" in normalized:
            queries.extend([
                "planetary habitability",
                "habitable zone",
                "exoplanet habitability",
                "potentially habitable exoplanets"
            ])

        # Extraterrestrial civilizations.
        if "civilization" in normalized:
            queries.extend([
                "extraterrestrial intelligence",
                "Search for extraterrestrial intelligence",
                "Drake equation"
            ])

        # Number of planets and stars.
        if "planet" in normalized and (
            "universe" in normalized or "exactly" in normalized
        ):
            queries.extend([
                "known planets in the universe",
                "exoplanet discoveries",
                "observable universe stars"
            ])

        unique = []
        seen = set()

        for query in queries:
            key = query.casefold().strip()
            if key and key not in seen:
                seen.add(key)
                unique.append(query.strip())

        return unique

    def _request_json(self, params: dict, timeout: int = 20) -> dict:
        for attempt in range(self.max_retries):

            elapsed = time.monotonic() - self.last_request_time

            if elapsed < self.request_interval:
                time.sleep(self.request_interval - elapsed)

            try:
                response = self.session.get(
                    self.api_url,
                    params=params,
                    timeout=timeout
                )

                self.last_request_time = time.monotonic()

                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    wait = (
                        int(retry_after)
                        if retry_after and retry_after.isdigit()
                        else 2 ** (attempt + 1)
                    )
                    time.sleep(wait)
                    continue

                response.raise_for_status()
                return response.json()

            except requests.RequestException:
                if attempt == self.max_retries - 1:
                    raise

                time.sleep(2 ** attempt)

        raise RuntimeError("Wikipedia API request failed after retries.")

    def search(self, claim: str, limit: int = 5) -> list[dict]:

        if not isinstance(claim, str) or not claim.strip():
            raise ValueError("Claim must be a non-empty string.")

        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
            raise ValueError("Limit must be a positive integer.")

        cache_key = (claim.strip().lower(), limit)

        cached = self.cache.get(cache_key)

        if cached:
            timestamp, evidence = cached

            if time.monotonic() - timestamp < self.cache_duration:
                return [dict(item) for item in evidence]

        try:
            # Search using expanded queries.
            page_scores = {}

            for query_index, query in enumerate(
                self._get_search_queries(claim)
            ):
                params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "srlimit": limit,
                    "format": "json"
                }

                data = self._request_json(params)

                results = (
                    data.get("query", {})
                    .get("search", [])
                )

                for position, result in enumerate(results):
                    page_id = str(result["pageid"])
                    title = result.get("title", "")

                    if page_id not in page_scores:
                        page_scores[page_id] = {
                            "title": title,
                            "score": 0
                        }

                    page_scores[page_id]["score"] += (
                        (limit - position) * (1.0 / (query_index + 1) ** 0.5)
                    )

            if not page_scores:
                self.cache[cache_key] = (time.monotonic(), [])
                return []

            ranked_pages = sorted(
                page_scores.items(),
                key=lambda item: item[1]["score"],
                reverse=True
            )

            selected_pages = ranked_pages[:limit]

            evidence = []
            seen_paragraphs = set()

            # Retrieve article extracts.
            for page_id, details in selected_pages:

                params = {
                    "action": "query",
                    "pageids": page_id,
                    "prop": "extracts",
                    "explaintext": 1,
                    "format": "json"
                }

                data = self._request_json(params, timeout=30)

                pages = (
                    data.get("query", {})
                    .get("pages", {})
                )

                page = pages.get(page_id, {})
                article_text = page.get("extract", "").strip()

                if not article_text:
                    continue

                paragraphs = [
                    p.strip()
                    for p in article_text.split("\n")
                    if len(p.strip()) >= 50
                ]

                # Prioritize early article paragraphs.
                for index, paragraph in enumerate(paragraphs[:5]):

                    normalized = re.sub(
                        r"\s+", " ", paragraph
                    ).casefold()

                    if normalized in seen_paragraphs:
                        continue

                    seen_paragraphs.add(normalized)

                    evidence.append({
                        "evidence_id": f"wiki_{page_id}_p{index + 1}",
                        "source": "Wikipedia",
                        "title": page.get("title", details["title"]),
                        "url": (
                            "https://en.wikipedia.org/"
                            f"?curid={page_id}"
                        ),
                        "text": paragraph
                    })

            self.cache[cache_key] = (
                time.monotonic(),
                [dict(item) for item in evidence]
            )

            return evidence

        except requests.RequestException as error:
            raise RuntimeError(
                f"Wikipedia retrieval failed: {error}"
            ) from error

        except (ValueError, KeyError, TypeError) as error:
            raise RuntimeError(
                f"Invalid Wikipedia API response: {error}"
            ) from error
