"""
routes/results.py — Retrieve upload history & individual results.
"""
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from db import get_db
from utils.auth import get_current_user

router = APIRouter(tags=["results"])


def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.get("/results")
async def list_results(
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Return all uploads for the authenticated user, newest first."""
    cursor = db["uploads"].find(
        {"user_id": current_user["user_id"]}
    ).sort("uploaded_at", -1).limit(50)

    results = []
    async for doc in cursor:
        results.append(_serialize(doc))
    return results


@router.get("/results/{upload_id}")
async def get_result(
    upload_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Return a single upload record by ID."""
    if not ObjectId.is_valid(upload_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    doc = await db["uploads"].find_one({
        "_id": ObjectId(upload_id),
        "user_id": current_user["user_id"],
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Upload not found")

    return _serialize(doc)
