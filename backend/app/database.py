from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    database_name = os.getenv("DATABASE_NAME", "anibot")

db = Database()

async def init_db():
    db.client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
    db.database = db.client[db.database_name]

async def close_db():
    db.client.close()