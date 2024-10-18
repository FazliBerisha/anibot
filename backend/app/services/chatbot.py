import httpx
import asyncio
import re
from typing import List, Optional
from app.models.user import User
from app.services.nlp import NLPService
import random

class ChatbotService:
    def __init__(self):
        self.nlp_service = NLPService()
        self.api_base_url = "https://api.jikan.moe/v4"
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        self.context = {}  # Add this line to store context
        self.last_recommendations = set()
        self.genre_mapping = {
            "action": 1, "adventure": 2, "comedy": 4, "drama": 8, "sci-fi": 24, "mystery": 7,
            "supernatural": 37, "fantasy": 10, "romance": 22, "thriller": 41, "crime": 7
        }

    async def process_message(self, message: str, user: Optional[User] = None) -> str:
        intent = self.nlp_service.classify_intent(message)
        keywords = self.nlp_service.extract_keywords(message)

        if intent == "recommendation" or intent == "random_recommendation":
            response = await self.handle_recommendation(keywords, random=intent == "random_recommendation")
            self.context['last_genre'] = next((kw for kw in keywords if kw in self.genre_mapping), None)
            return response
        elif intent == "trending":
            return await self.handle_trending()
        elif intent == "popular_in_genre":
            return await self.handle_popular_in_genre(keywords)
        elif intent == "information":
            return await self.handle_information(keywords)
        elif intent == "most_popular":
            return await self.handle_most_popular()
        else:
            return "I'm sorry, I don't understand that request. Could you please try asking for recommendations, trending anime, or information about a specific anime?"

    async def make_api_request(self, endpoint: str, params: dict = None) -> dict:
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{self.api_base_url}/{endpoint}", params=params, timeout=10.0)
                    response.raise_for_status()
                    return response.json()
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError) as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed to connect to the API after {self.max_retries} attempts. Please try again later.")
                await asyncio.sleep(self.retry_delay * (attempt + 1))
            except httpx.HTTPStatusError as e:
                raise Exception(f"API returned an error: {e.response.status_code} {e.response.reason_phrase}")

    async def handle_follow_up(self, message: str) -> str:
        if any(word in message.lower() for word in ["episode", "how many"]):
            anime_name = self.extract_anime_name(message) or self.context.get('last_anime')
            if anime_name:
                return await self.get_episode_count(anime_name)
            else:
                return "I'm sorry, I couldn't determine which anime you're asking about. Could you please specify the anime name?"
        elif "different" in message.lower():
            return await self.handle_recommendation(self.context.get('last_keywords', []), different=True)
        return "I'm sorry, I didn't understand your follow-up question. Could you please rephrase or ask a new question?"

    def extract_anime_name(self, message: str) -> Optional[str]:
        words = message.lower().split()
        if "is" in words:
            return " ".join(words[words.index("is")+1:])
        return None

    async def handle_recommendation(self, keywords: List[str], random: bool = False) -> str:
        genre = next((kw for kw in keywords if kw in self.genre_mapping), None)
        if not genre:
            return "I'm sorry, I couldn't identify a specific genre. Could you please specify a genre like action, comedy, romance, crime, etc.?"

        try:
            params = {
                "genres": str(self.genre_mapping[genre]),
                "order_by": "score" if not random else "random",
                "sort": "desc",
                "limit": 5 if not random else 1
            }
            data = await self.make_api_request("anime", params=params)
            if random:
                anime = data['data'][0]
                return f"Here's a random {genre} anime recommendation: {anime['title']}. {anime['synopsis'][:100]}..."
            else:
                recommendations = [anime['title'] for anime in data['data'][:5]]
                return f"Here are some {genre} anime recommendations: {', '.join(recommendations)}"
        except Exception as e:
            return f"I'm sorry, I couldn't fetch {genre} anime recommendations at the moment. Error: {str(e)}"

    async def handle_information(self, keywords: List[str]) -> str:
        search_query = " ".join(keywords)
        try:
            data = await self.make_api_request("anime", params={"q": search_query, "limit": 1})
            if data['data']:
                anime = data['data'][0]
                self.context['last_anime'] = anime['title']
                episodes = anime['episodes'] if anime['episodes'] is not None else "Unknown"
                synopsis = anime['synopsis'][:200] + "..." if len(anime['synopsis']) > 200 else anime['synopsis']
                return f"{anime['title']}: {synopsis}\n\nAdditional Information: Episodes: {episodes}, Status: {anime['status']}, Score: {anime['score']}"
            else:
                return f"I'm sorry, I couldn't find any information about {search_query}."
        except Exception as e:
            return f"I'm sorry, I couldn't fetch the information at the moment. Error: {str(e)}"

    async def handle_trending(self) -> str:
        try:
            data = await self.make_api_request("top/anime", params={"filter": "airing", "limit": 5})
            trending = [anime['title'] for anime in data['data'][:5]]
            return f"Some trending anime right now are: {', '.join(trending)}"
        except Exception as e:
            return f"I'm sorry, I couldn't fetch the trending anime at the moment. Error: {str(e)}"

    async def handle_genre_recommendation(self, keywords: List[str]) -> str:
        genre = next((keyword for keyword in keywords if keyword in self.nlp_service.genres), None)
        params = {"order_by": "score", "sort": "desc", "limit": 10}
        if genre:
            params["genres"] = self.nlp_service.genre_mapping.get(genre)
        
        try:
            data = await self.make_api_request("anime", params=params)
            if data['data']:
                recommendations = [anime['title'] for anime in data['data'] if anime['title'] not in self.last_recommendations]
                if not recommendations:
                    recommendations = [anime['title'] for anime in data['data']]
                selected = random.sample(recommendations, min(5, len(recommendations)))
                self.last_recommendations.update(selected)
                return f"Here are some anime recommendations: {', '.join(selected)}"
            else:
                return "I'm sorry, I couldn't find any recommendations at the moment."
        except Exception as e:
            return f"I'm sorry, I couldn't fetch recommendations at the moment. Error: {str(e)}"

    async def get_episode_count(self, anime: str) -> str:
        try:
            data = await self.make_api_request("anime", params={"q": anime, "limit": 1})
            if data['data']:
                episodes = data['data'][0]['episodes']
                return f"{anime} has {episodes} episodes." if episodes else f"The number of episodes for {anime} is unknown or ongoing."
            return f"I'm sorry, I couldn't find episode information for {anime}."
        except Exception as e:
            return f"I'm sorry, I couldn't fetch the episode count for {anime} at the moment. Error: {str(e)}"

    async def handle_popular_in_genre(self, keywords: List[str]) -> str:
        genre = next((kw for kw in keywords if kw in self.genre_mapping), None)
        if not genre:
            return "I'm sorry, I couldn't identify a specific genre. Could you please specify a genre like action, comedy, romance, crime, etc.?"

        try:
            data = await self.make_api_request("anime", params={
                "genres": str(self.genre_mapping[genre]),
                "order_by": "popularity",
                "sort": "asc",
                "limit": 5
            })
            popular = [anime['title'] for anime in data['data'][:5]]
            return f"Some popular {genre} anime are: {', '.join(popular)}"
        except Exception as e:
            return f"I'm sorry, I couldn't fetch popular {genre} anime at the moment. Error: {str(e)}"

    async def handle_most_popular(self) -> str:
        genre = self.context.get('last_genre')
        if not genre:
            return "I'm sorry, I couldn't determine which genre you're referring to. Could you please specify a genre like action, comedy, romance, crime, etc.?"

        try:
            data = await self.make_api_request("anime", params={
                "genres": str(self.genre_mapping[genre]),
                "order_by": "popularity",
                "sort": "asc",
                "limit": 1
            })
            if data['data']:
                anime = data['data'][0]
                return f"The most popular {genre} anime is: {anime['title']}. {anime['synopsis'][:100]}..."
            else:
                return f"I'm sorry, I couldn't find the most popular {genre} anime at the moment."
        except Exception as e:
            return f"I'm sorry, I couldn't fetch the most popular {genre} anime at the moment. Error: {str(e)}"
