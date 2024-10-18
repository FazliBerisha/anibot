from fastapi import APIRouter, HTTPException, Depends
from app.models import Rating, RatingCreate, User
from app.database import db
from app.auth import get_current_user
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/ratings/", response_model=Rating)
async def create_rating(rating: RatingCreate, current_user: User = Depends(get_current_user)):
    rating_dict = rating.dict()
    rating_dict["user_id"] = current_user.id
    new_rating = await db.database["ratings"].insert_one(rating_dict)
    created_rating = await db.database["ratings"].find_one({"_id": new_rating.inserted_id})
    return Rating(**created_rating)

@router.get("/ratings/{rating_id}", response_model=Rating)
async def read_rating(rating_id: str, current_user: User = Depends(get_current_user)):
    rating = await db.database["ratings"].find_one({"_id": ObjectId(rating_id)})
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return Rating(**rating)

@router.get("/ratings/", response_model=List[Rating])
async def list_ratings(skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user)):
    ratings = await db.database["ratings"].find().skip(skip).limit(limit).to_list(limit)
    return [Rating(**rating) for rating in ratings]

@router.get("/ratings/anime/{anime_id}", response_model=List[Rating])
async def get_anime_ratings(anime_id: str, skip: int = 0, limit: int = 10):
    ratings = await db.database["ratings"].find({"anime_id": ObjectId(anime_id)}).skip(skip).limit(limit).to_list(limit)
    return [Rating(**rating) for rating in ratings]

@router.get("/ratings/user/me", response_model=List[Rating])
async def get_user_ratings(current_user: User = Depends(get_current_user), skip: int = 0, limit: int = 10):
    ratings = await db.database["ratings"].find({"user_id": current_user.id}).skip(skip).limit(limit).to_list(limit)
    return [Rating(**rating) for rating in ratings]