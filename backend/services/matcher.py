"""
matcher.py — Compare hashes and classify similarity.
"""
from typing import List
import imagehash


# ── Thresholds ────────────────────────────────────────────────────────────────
# pHash is a 64-bit hash; max hamming distance = 64
AUTHORIZED_THRESHOLD = 85   # similarity % ≥ this → Authorized
SUSPICIOUS_THRESHOLD = 50   # similarity % ≥ this → Suspicious (else No Match)


# ── Core helpers ──────────────────────────────────────────────────────────────

def hamming_distance(hash1: str, hash2: str) -> int:
    """Compute bit-level Hamming distance between two pHash strings."""
    try:
        h1 = imagehash.hex_to_hash(hash1)
        h2 = imagehash.hex_to_hash(hash2)
        return h1 - h2          # imagehash overloads '-' as Hamming distance
    except Exception:
        return 64               # treat parse errors as maximum distance


def similarity_score(hash1: str, hash2: str) -> float:
    """
    Convert Hamming distance to a 0–100 similarity percentage.
    pHash uses 64 bits → distance 0 means identical, 64 means completely different.
    """
    dist = hamming_distance(hash1, hash2)
    return round((1 - dist / 64) * 100, 2)


def classify(score: float) -> str:
    """Return status label based on similarity percentage."""
    if score >= AUTHORIZED_THRESHOLD:
        return "Authorized"
    elif score >= SUSPICIOUS_THRESHOLD:
        return "Suspicious"
    return "No Match"


# ── Multi-hash matching (for videos) ─────────────────────────────────────────

def best_score_across_hashes(query_hashes: List[str], db_hashes: List[str]) -> float:
    """
    Given two lists of hashes (e.g. video frame hashes), return the highest
    pairwise similarity score.
    """
    best = 0.0
    for qh in query_hashes:
        for dh in db_hashes:
            s = similarity_score(qh, dh)
            if s > best:
                best = s
    return best


def compare_with_dataset(
    query_hashes: List[str],
    dataset: List[dict],       # list of {id, name, phash, all_hashes, file_path}
) -> List[dict]:
    """
    Compare query hashes against every dataset entry.
    Returns sorted list of match dicts (highest similarity first).
    """
    results = []
    for entry in dataset:
        db_hashes = entry.get("all_hashes") or [entry["phash"]]
        score = best_score_across_hashes(query_hashes, db_hashes)
        dist = hamming_distance(query_hashes[0], db_hashes[0])
        status = classify(score)
        results.append({
            "dataset_id": str(entry.get("_id", entry.get("id", ""))),
            "dataset_name": entry["name"],
            "similarity": score,
            "hamming_distance": dist,
            "status": status,
            "thumbnail": entry.get("file_path"),
        })

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results
