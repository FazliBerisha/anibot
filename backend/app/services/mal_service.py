import httpx
from typing import Dict, List, Optional

class MALService:
    BASE_URL = "https://api.jikan.moe/v4"

    @staticmethod
    async def search_anime(query: str) -> Optional[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MALService.BASE_URL}/anime", params={"q": query, "limit": 1})
            if response.status_code == 200:
                data = response.json()
                if data["data"]:
                    return data["data"][0]
            return None

    @staticmethod
    async def get_anime_by_id(anime_id: int) -> Optional[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MALService.BASE_URL}/anime/{anime_id}")
            if response.status_code == 200:
                return response.json()["data"]
            return None

    @staticmethod
    async def get_top_anime(limit: int = 10) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MALService.BASE_URL}/top/anime", params={"limit": limit})
            if response.status_code == 200:
                return response.json()["data"]
            return []

    @staticmethod
    async def get_anime_by_genre(genre: str, limit: int = 3) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MALService.BASE_URL}/anime", params={"genre": genre, "limit": limit, "order_by": "score", "sort": "desc"})
            if response.status_code == 200:
                return response.json()["data"]
            return []
