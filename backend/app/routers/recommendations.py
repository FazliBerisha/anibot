from fastapi import APIRouter, Depends
from app.models import User, Anime
from app.auth import get_current_user
from app.services.recommendation import RecommendationService
from typing import List

router = APIRouter()

@router.get("/recommendations/", response_model=List[Anime])
async def get_recommendations(current_user: User = Depends(get_current_user)):
    recommendations = await RecommendationService.get_recommendations(str(current_user.id))
    return recommendations