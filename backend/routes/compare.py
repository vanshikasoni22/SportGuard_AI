"""
routes/compare.py — Ad-hoc compare two files without persisting.
"""
import os
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from db import get_db
from utils.auth import get_current_user
from services.fingerprint import fingerprint_file
from services.matcher import similarity_score, hamming_distance, classify

router = APIRouter(tags=["compare"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


@router.post("/compare")
async def compare_two_files(
    file_a: UploadFile = File(...),
    file_b: UploadFile = File(...),
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Compare two uploaded files directly and return similarity metrics."""
    results = {}
    tmp_paths = []

    for label, file in [("a", file_a), ("b", file_b)]:
        ext = Path(file.filename).suffix.lower()
        tmp_path = os.path.join(UPLOAD_DIR, f"tmp_{uuid.uuid4()}{ext}")
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        tmp_paths.append(tmp_path)
        fp = fingerprint_file(tmp_path)
        results[label] = fp

    score = similarity_score(results["a"]["phash"], results["b"]["phash"])
    dist = hamming_distance(results["a"]["phash"], results["b"]["phash"])
    status = classify(score)

    # Clean up temp files
    for p in tmp_paths:
        try:
            os.remove(p)
        except OSError:
            pass

    return {
        "file_a": file_a.filename,
        "file_b": file_b.filename,
        "hash_a": results["a"]["phash"],
        "hash_b": results["b"]["phash"],
        "similarity": score,
        "hamming_distance": dist,
        "status": status,
    }
