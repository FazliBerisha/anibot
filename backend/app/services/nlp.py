import spacy
from typing import List, Tuple

class NLPService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.genres = ["action", "adventure", "comedy", "drama", "sci-fi", "mystery", "supernatural", "fantasy", "romance", "thriller", "crime"]
        self.genre_mapping = {
            "action": 1, "adventure": 2, "comedy": 4, "drama": 8, "sci-fi": 24, "mystery": 7,
            "supernatural": 37, "fantasy": 10, "romance": 22, "thriller": 41, "crime": 7
        }
        self.genre_keywords = {
            "romance": ["romance", "romantic", "love"],
            "crime": ["crime", "detective", "mystery"],
            # Add more genre keywords as needed
        }

    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    def classify_intent(self, message: str) -> str:
        message = message.lower()
        if any(word in message for word in ["recommend", "suggestion", "give me", "how about", "what are some"]):
            return "recommendation"
        if "trending" in message:
            return "trending"
        if "popular" in message:
            return "popular_in_genre"
        if any(word in message for word in ["what is", "tell me about", "info"]):
            return "information"
        return "unknown"

    def extract_keywords(self, message: str) -> List[str]:
        message = message.lower()
        extracted_genres = []
        for genre, keywords in self.genre_keywords.items():
            if any(keyword in message for keyword in keywords):
                extracted_genres.append(genre)
        return extracted_genres or [word for word in message.split() if word in self.genres]
