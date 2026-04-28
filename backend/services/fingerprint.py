"""
fingerprint.py — Generate perceptual hashes for images and videos.
"""
import os
from pathlib import Path
from typing import List

import imagehash
import cv2
from PIL import Image


# ── Image fingerprinting ──────────────────────────────────────────────────────

def hash_image(file_path: str) -> str:
    """Return pHash string for an image file."""
    img = Image.open(file_path).convert("RGB")
    return str(imagehash.phash(img))


# ── Video fingerprinting ──────────────────────────────────────────────────────

def hash_video(file_path: str, max_frames: int = 10) -> List[str]:
    """
    Extract up to `max_frames` evenly-spaced key frames from a video
    and return their pHash strings.
    """
    cap = cv2.VideoCapture(file_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        cap.release()
        return []

    step = max(1, total_frames // max_frames)
    hashes: List[str] = []

    frame_idx = 0
    while cap.isOpened() and len(hashes) < max_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break
        # Convert BGR → RGB PIL image
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        hashes.append(str(imagehash.phash(pil_img)))
        frame_idx += step

    cap.release()
    return hashes


# ── Unified entry point ───────────────────────────────────────────────────────

def fingerprint_file(file_path: str) -> dict:
    """
    Detect whether the file is an image or video, generate hashes,
    and return a dict with:
        media_type: "image" | "video"
        phash:      primary hash string
        all_hashes: list of all hashes (single item for image)
    """
    ext = Path(file_path).suffix.lower()
    video_exts = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

    if ext in video_exts:
        hashes = hash_video(file_path)
        primary = hashes[0] if hashes else "0" * 16
        return {"media_type": "video", "phash": primary, "all_hashes": hashes}
    else:
        h = hash_image(file_path)
        return {"media_type": "image", "phash": h, "all_hashes": [h]}
