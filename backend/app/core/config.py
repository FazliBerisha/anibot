from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "anibot"

    class Config:
        env_file = ".env"

settings = Settings()

