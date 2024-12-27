from motor.motor_asyncio import AsyncIOMotorClient
from ..config import get_settings

settings = get_settings()

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db = MongoDB()

async def get_database():
    return db.db

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    db.db = db.client[settings.mongodb_db]

async def close_mongo_connection():
    db.client.close()
