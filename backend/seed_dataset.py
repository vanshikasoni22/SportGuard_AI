"""
seed_dataset.py — Populate MongoDB with simulated dataset entries.

Run once after generate_dataset.py:
    python seed_dataset.py
"""
import os
import asyncio
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from motor.motor_asyncio import AsyncIOMotorClient
import imagehash
from PIL import Image

from generate_dataset import generate

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME",   "sportguard")


def phash_file(path: str) -> str:
    img = Image.open(path).convert("RGB")
    return str(imagehash.phash(img))


async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    # Drop existing dataset
    await db["dataset"].drop()
    print("🗑️  Cleared existing dataset collection.")

    # Generate images
    items = generate()

    # Group originals first to link variants
    originals_map: dict[str, str] = {}   # team_name → inserted_id (str)

    docs = []
    for item in items:
        path = item["path"]
        if not Path(path).exists():
            print(f"⚠️  File not found, skipping: {path}")
            continue

        phash = phash_file(path)
        doc = {
            "name": item["name"],
            "description": f"Simulated media for {item['team']}",
            "file_path": path,
            "phash": phash,
            "all_hashes": [phash],
            "is_original": item["is_original"],
            "team": item["team"],
            "registered_at": datetime.utcnow(),
        }
        docs.append((item, doc))

    # Insert originals first
    for item, doc in docs:
        if item["is_original"]:
            result = await db["dataset"].insert_one(doc)
            originals_map[item["team"]] = str(result.inserted_id)
            print(f"  ✅ Original  — {doc['name']}  | pHash: {doc['phash']}")

    # Insert variants with parent_id
    for item, doc in docs:
        if not item["is_original"]:
            doc["parent_id"] = originals_map.get(item["team"])
            result = await db["dataset"].insert_one(doc)
            print(f"  ⚠️  Variant   — {doc['name']}  | pHash: {doc['phash']}")

    total = await db["dataset"].count_documents({})
    print(f"\n🎉  Seeding complete — {total} entries in '{DB_NAME}.dataset'")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
