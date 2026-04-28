"""
routes/auth.py — Register & Login endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from models.media import UserCreate, UserOut
from utils.auth import hash_password, verify_password, create_access_token
from db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=dict)
async def register(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    existing = await db["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    doc = {
        "email": user.email,
        "name": user.name,
        "hashed_password": hash_password(user.password),
        "created_at": datetime.utcnow(),
    }
    result = await db["users"].insert_one(doc)
    token = create_access_token({"sub": str(result.inserted_id), "email": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": str(result.inserted_id), "email": user.email, "name": user.name},
    }


@router.post("/login", response_model=dict)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    user = await db["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["_id"]), "email": user["email"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": str(user["_id"]), "email": user["email"], "name": user.get("name", "")},
    }
