"""
routes/upload.py — Upload media, fingerprint, compare, persist result.
"""
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from db import get_db
from utils.auth import get_current_user
from services.fingerprint import fingerprint_file
from services.matcher import compare_with_dataset
from services.dataset import get_all_dataset_entries

router = APIRouter(tags=["upload"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
}


@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    # Save file
    unique_name = f"{uuid.uuid4()}{ext}"
    save_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Fingerprint
    fp = fingerprint_file(save_path)

    # Compare against dataset
    dataset = await get_all_dataset_entries(db)
    raw_matches = compare_with_dataset(fp["all_hashes"], dataset)

    # Top result
    top = raw_matches[0] if raw_matches else None
    top_status = top["status"] if top else "No Match"
    top_similarity = top["similarity"] if top else 0.0

    # Persist
    doc = {
        "user_id": current_user["user_id"],
        "filename": file.filename,
        "file_path": save_path,
        "media_type": fp["media_type"],
        "phash": fp["phash"],
        "all_hashes": fp["all_hashes"],
        "matches": raw_matches[:10],     # keep top 10 matches
        "top_status": top_status,
        "top_similarity": top_similarity,
        "uploaded_at": datetime.utcnow(),
    }
    result = await db["uploads"].insert_one(doc)

    return {
        "id": str(result.inserted_id),
        "filename": file.filename,
        "media_type": fp["media_type"],
        "phash": fp["phash"],
        "top_status": top_status,
        "top_similarity": top_similarity,
        "matches": raw_matches[:10],
        "file_url": f"/uploads/{unique_name}",
    }
