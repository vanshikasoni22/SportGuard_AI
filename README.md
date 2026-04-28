# SportGuard AI 🛡️

> **AI-Powered Sports Media Tracking & Unauthorized Content Detection**  
> Hackathon MVP — perceptual fingerprinting + similarity matching + real-time dashboard

---

## 🧠 How It Works

```
Upload Image/Video
       ↓
Perceptual Hash (pHash via ImageHash + OpenCV frame extraction)
       ↓
Compare against registered dataset (Hamming distance)
       ↓
Similarity Score (0–100%) → Status classification
       ↓
Dashboard: ✅ Authorized / ⚠️ Suspicious / ❌ No Match
```

**Thresholds:**
| Similarity | Status |
|---|---|
| ≥ 85% | ✅ Authorized — exact or near-exact copy |
| 50–84% | ⚠️ Suspicious — modified/cropped/filtered copy |
| < 50% | ❌ No Match — unrelated content |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite + Chart.js |
| Backend | FastAPI (Python 3.10+) |
| AI/Hashing | ImageHash (pHash) + OpenCV |
| Database | MongoDB (via Motor async driver) |
| Auth | JWT + bcrypt |

---

## 📁 Folder Structure

```
SportGuard_AI/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── db.py                    # MongoDB Motor connection
│   ├── routes/
│   │   ├── auth.py              # POST /auth/register, /auth/login
│   │   ├── upload.py            # POST /upload
│   │   ├── results.py           # GET /results, /results/{id}
│   │   └── compare.py           # POST /compare
│   ├── services/
│   │   ├── fingerprint.py       # pHash for images & videos
│   │   ├── matcher.py           # Hamming distance + classification
│   │   └── dataset.py           # MongoDB dataset queries
│   ├── models/
│   │   └── media.py             # Pydantic models
│   ├── utils/
│   │   └── auth.py              # JWT + bcrypt helpers
│   ├── generate_dataset.py      # Create sample PNG images
│   ├── seed_dataset.py          # Populate MongoDB with dataset
│   ├── dataset_media/           # Generated sample images (auto-created)
│   ├── uploads/                 # Uploaded files (auto-created)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── UploadPanel.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── SimilarityChart.jsx
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── .env
│   └── vite.config.js
├── .env.example
└── README.md
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB running locally on `mongodb://localhost:27017`

> **Start MongoDB:**  
> `brew services start mongodb-community` (macOS)  
> or `mongod --dbpath /data/db` (Linux)

---

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp ../.env.example .env        # Edit if needed (default values work locally)

# Generate sample dataset images
python generate_dataset.py

# Seed MongoDB with dataset
python seed_dataset.py

# Start FastAPI server
uvicorn main:app --reload --port 8000
```

Backend will be live at: **http://localhost:8000**  
Interactive API docs: **http://localhost:8000/docs**

---

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies (already done if you ran npm install)
npm install

# Start dev server
npm run dev
```

Frontend will be live at: **http://localhost:5173**

---

## 🎬 Demo Steps

1. **Open** http://localhost:5173
2. **Register** a new account (any email + password)
3. **Upload** one of the generated sample images from `backend/dataset_media/`
   - Try `FC_Blaze_original.png` → expect **✅ Authorized** (~100%)
   - Try `FC_Blaze_crop.png` → expect **⚠️ Suspicious** (~70–85%)
   - Try `FC_Blaze_filter.png` → expect **⚠️ Suspicious** (~55–75%)
   - Upload a completely different image → expect **❌ No Match**
4. **View** the similarity distribution chart
5. **Check** Scan History table at the bottom

---

## 🔌 API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Register new user |
| POST | `/auth/login` | No | Login, get JWT |
| POST | `/upload` | Yes | Upload + fingerprint + compare |
| GET | `/results` | Yes | List all uploads |
| GET | `/results/{id}` | Yes | Single upload detail |
| POST | `/compare` | Yes | Compare two files directly |
| GET | `/health` | No | Health check |

---

## 🧪 Sample Dataset

25 images auto-generated across 5 teams × 5 variants:

| Team | Variants |
|---|---|
| FC Blaze | original, crop, resize, filter, tint |
| Ocean United | original, crop, resize, filter, tint |
| GreenStorm FC | original, crop, resize, filter, tint |
| Thunder Hawks | original, crop, resize, filter, tint |
| Iron Wolves | original, crop, resize, filter, tint |

---

## 🔒 Security Notes

- JWT tokens expire after 60 minutes (configurable via `JWT_EXPIRE_MINUTES`)
- Passwords hashed with bcrypt
- Change `JWT_SECRET` in `.env` before any deployment

---

## 🚀 Built for Hackathon Demo

Focus: clean working prototype demonstrating perceptual fingerprinting and similarity detection. Not production-ready — designed for demo purposes.
