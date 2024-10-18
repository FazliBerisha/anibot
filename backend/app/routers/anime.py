from fastapi import APIRouter, HTTPException, Depends
from app.models import Anime, AnimeCreate, AnimeUpdate, User
from app.database import db
from app.auth import get_current_user
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/anime/", response_model=Anime)
async def create_anime(anime: AnimeCreate, current_user: User = Depends(get_current_user)):
    new_anime = await db.database["animes"].insert_one(anime.dict())
    created_anime = await db.database["animes"].find_one({"_id": new_anime.inserted_id})
    return Anime(**created_anime)

@router.get("/anime/{anime_id}", response_model=Anime)
async def read_anime(anime_id: str):
    anime = await db.database["animes"].find_one({"_id": ObjectId(anime_id)})
    if anime is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return Anime(**anime)

@router.get("/anime/", response_model=List[Anime])
async def list_animes(skip: int = 0, limit: int = 10):
    animes = await db.database["animes"].find().skip(skip).limit(limit).to_list(limit)
    return [Anime(**anime) for anime in animes]

@router.put("/anime/{anime_id}", response_model=Anime)
async def update_anime(anime_id: str, anime_update: AnimeUpdate, current_user: User = Depends(get_current_user)):
    updated_anime = await db.database["animes"].find_one_and_update(
        {"_id": ObjectId(anime_id)},
        {"$set": anime_update.dict(exclude_unset=True)},
        return_document=True
    )
    if updated_anime is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return Anime(**updated_anime)

@router.delete("/anime/{anime_id}", response_model=dict)
async def delete_anime(anime_id: str, current_user: User = Depends(get_current_user)):
    delete_result = await db.database["animes"].delete_one({"_id": ObjectId(anime_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Anime not found")
    return {"message": "Anime deleted successfully"}
