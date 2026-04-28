"""
main.py — FastAPI application entry point for SportGuard AI.
"""
import os
from pathlib import Path
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db import get_client, close_db
from routes.auth import router as auth_router
from routes.upload import router as upload_router
from routes.results import router as results_router
from routes.compare import router as compare_router

# ── Startup / Shutdown ────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure upload directory exists
    upload_dir = os.getenv("UPLOAD_DIR", "uploads")
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    # Touch MongoDB connection
    get_client()
    yield
    await close_db()


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="SportGuard AI",
    description="AI-Powered Sports Media Tracking & Unauthorized Content Detection",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static uploads ────────────────────────────────────────────────────────────

upload_dir = os.getenv("UPLOAD_DIR", "uploads")
Path(upload_dir).mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# ── Dataset media static files ─────────────────────────────────────────────────

dataset_dir = Path("dataset_media")
dataset_dir.mkdir(parents=True, exist_ok=True)
app.mount("/dataset_media", StaticFiles(directory=str(dataset_dir)), name="dataset_media")

# ── Routers ───────────────────────────────────────────────────────────────────

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(results_router)
app.include_router(compare_router)


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "SportGuard AI"}
