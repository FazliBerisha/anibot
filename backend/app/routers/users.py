from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models import User, UserCreate, UserInDB, Token
from app.database import db
from app.auth import get_password_hash, authenticate_user, create_access_token, get_current_user, verify_password
from bson import ObjectId
from typing import List
from datetime import timedelta

router = APIRouter()

@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    db_user = await db.database["users"].find_one({"username": user.username})
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)
    new_user = await db.database["users"].insert_one(user_in_db.dict())
    created_user = await db.database["users"].find_one({"_id": new_user.inserted_id})
    return User(**created_user)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str, current_user: User = Depends(get_current_user)):
    user = await db.database["users"].find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)

@router.get("/users/", response_model=List[User])
async def list_users(skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user)):
    users = await db.database["users"].find().skip(skip).limit(limit).to_list(limit)
    return [User(**user) for user in users]
