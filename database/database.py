from motor.motor_asyncio import AsyncIOMotorClient
from schemes.settings import get_settings

settings = get_settings()

client = AsyncIOMotorClient(settings.MONGO_URL)
database = client.taskdb
