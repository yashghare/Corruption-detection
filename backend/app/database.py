# backend/app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

# MongoDB connection
client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.MONGODB_NAME]

# Collections
transactions = db["transactions"]

# Remove all SQLAlchemy-related code