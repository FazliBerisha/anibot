from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.token import TokenData
from app.models.user import User
from app.database import db
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Temporarily bypass token validation
    return User(id="test", username="testuser", email="test@example.com")
