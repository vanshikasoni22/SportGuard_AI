from bson import ObjectId
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ── helpers ──────────────────────────────────────────────────────────────────

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# ── User ─────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class UserInDB(BaseModel):
    id: Optional[str] = None
    email: str
    name: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserOut(BaseModel):
    id: Optional[str] = None
    email: str
    name: str


# ── Media / Upload ────────────────────────────────────────────────────────────

class MatchResult(BaseModel):
    dataset_id: str
    dataset_name: str
    similarity: float          # 0–100
    hamming_distance: int
    status: str                # Authorized | Suspicious | No Match
    thumbnail: Optional[str] = None


class UploadRecord(BaseModel):
    id: Optional[str] = None
    user_id: str
    filename: str
    file_path: str
    media_type: str            # image | video
    phash: str                 # primary hash (image or first key frame)
    all_hashes: List[str] = [] # extra frame hashes for video
    matches: List[MatchResult] = []
    top_status: str = "No Match"
    top_similarity: float = 0.0
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


# ── Dataset entry (simulated) ─────────────────────────────────────────────────

class DatasetEntry(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    file_path: str
    phash: str
    is_original: bool
    parent_id: Optional[str] = None   # points to original if this is a variant
    registered_at: datetime = Field(default_factory=datetime.utcnow)
