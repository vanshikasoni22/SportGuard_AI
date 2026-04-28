"""
db.py — MongoDB async connection via Motor.
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

_client: AsyncIOMotorClient = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        _client = AsyncIOMotorClient(uri)
    return _client


def get_db() -> AsyncIOMotorDatabase:
    """FastAPI dependency — returns the database handle."""
    db_name = os.getenv("DB_NAME", "sportguard")
    return get_client()[db_name]


async def close_db():
    global _client
    if _client is not None:
        _client.close()
        _client = None
