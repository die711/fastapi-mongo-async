from motor.motor_asyncio import AsyncIOMotorClient
from schemes.settings import Settings

settings = Settings()

client = AsyncIOMotorClient(settings.MONGO_URL)
database = client.taskdb
