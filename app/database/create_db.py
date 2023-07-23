from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

MONGO_URL = settings.MONGO_URL
MONGO_DB = settings.MONGO_DB


client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]
