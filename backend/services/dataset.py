"""
dataset.py — Seed + retrieve the simulated media dataset from MongoDB.
"""
import os
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime


DATASET_COLLECTION = "dataset"


async def get_all_dataset_entries(db: AsyncIOMotorDatabase) -> list:
    """Return all dataset entries as plain dicts."""
    cursor = db[DATASET_COLLECTION].find({})
    entries = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        entries.append(doc)
    return entries


async def get_dataset_count(db: AsyncIOMotorDatabase) -> int:
    return await db[DATASET_COLLECTION].count_documents({})
