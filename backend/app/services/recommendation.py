from app.database import db
from app.models import Anime, Rating
from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationService:
    @staticmethod
    async def get_user_ratings(user_id: str) -> List[Rating]:
        ratings = await db.database["ratings"].find({"user_id": user_id}).to_list(None)
        return [Rating(**rating) for rating in ratings]

    @staticmethod
    async def get_all_animes() -> List[Anime]:
        animes = await db.database["animes"].find().to_list(None)
        return [Anime(**anime) for anime in animes]

    @staticmethod
    def create_user_item_matrix(users, items, ratings):
        matrix = np.zeros((len(users), len(items)))
        user_indices = {user: i for i, user in enumerate(users)}
        item_indices = {str(item.id): i for i, item in enumerate(items)}
        
        for rating in ratings:
            user_idx = user_indices[str(rating.user_id)]
            item_idx = item_indices[str(rating.anime_id)]
            matrix[user_idx, item_idx] = rating.score
        
        return matrix

    @staticmethod
    async def get_recommendations(user_id: str, n: int = 5) -> List[Anime]:
        user_ratings = await RecommendationService.get_user_ratings(user_id)
        all_animes = await RecommendationService.get_all_animes()
        all_users = await db.database["users"].distinct("_id")
        all_ratings = await db.database["ratings"].find().to_list(None)

        user_item_matrix = RecommendationService.create_user_item_matrix(all_users, all_animes, all_ratings)
        
        user_idx = list(all_users).index(user_id)
        user_ratings = user_item_matrix[user_idx]
        
        # Calculate similarity between the user and all items
        item_similarity = cosine_similarity([user_ratings], user_item_matrix.T)[0]
        
        # Get indices of top N similar items
        similar_indices = item_similarity.argsort()[::-1][:n]
        
        # Get the corresponding anime objects
        recommended_animes = [all_animes[idx] for idx in similar_indices if user_ratings[idx] == 0]
        
        return recommended_animes[:n]