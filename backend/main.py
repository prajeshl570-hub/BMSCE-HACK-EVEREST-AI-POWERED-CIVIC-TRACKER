import hashlib
import os
import sqlite3
import torch
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from pydantic import BaseModel

app = FastAPI()


# --- CONFIG ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "sqlite_fallback.db")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# --- AI MODEL ---
device = 'cuda' if torch.cuda.is_available() else 'cpu'
try:
    yolo_model = YOLO("best.pt").to(device)
    print(f"✅ AI Model loaded on {device}")
except Exception as e:
    print(f"⚠️ AI Bypass: {e}")
    yolo_model = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE ---
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, email TEXT UNIQUE, password TEXT,
            points INTEGER DEFAULT 0, role TEXT DEFAULT 'citizen'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS civic_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL, lng REAL, image_hash TEXT UNIQUE,
            category TEXT, resolved BOOLEAN DEFAULT 0, 
            user_name TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()
# 1. FIX: Missing /get-locations
@app.get("/get-locations")
async def get_locations():
    # Replace this with your actual database fetch logic
    # Example mock data:
    return [
        {"id": 1, "lat": 12.9716, "lng": 77.5946, "category": "trash", "user_name": "Citizen", "resolved": False},
        {"id": 2, "lat": 12.9352, "lng": 77.6245, "category": "pothole", "user_name": "Agent", "resolved": True}
    ]

# 2. FIX: Missing /upload
@app.post("/upload")
async def upload_issue(
    name: str = Form(...),
    description: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    image: UploadFile = File(...)
):
    # YOUR YOLO LOGIC GOES HERE
    # result = model.predict(image)
    
    # Example Success Response
    return {
        "status": "success",
        "category": description, # or whatever the AI detects
        "detail": "Issue reported successfully"
    }

# 3. FIX: Missing /resolve-issue (for the Staff Dashboard)
@app.post("/resolve-issue/{issue_id}")
async def resolve_issue(issue_id: int):
    # db.execute("UPDATE reports SET resolved = True WHERE id = ?", (issue_id,))
    return {"status": "success", "message": f"Issue {issue_id} resolved"}


@app.post("/register")
async def register(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    hashed = pwd_context.hash(password)
    # Automatically grant staff role if email contains keywords
    role = "staff" if any(x in email.lower() for x in ["admin", "staff"]) else "citizen"
    conn = get_db()
    try:
        conn.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", (name, email, hashed, role))
        conn.commit()
        return {"status": "success", "role": role}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    finally:
        conn.close()

@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    
    if not user or not pwd_context.verify(password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "name": user['name'], 
        "email": user['email'], 
        "is_staff": user['role'] == "staff",
        "points": user['points']
    }

# --- REMAINING ENDPOINTS (Upload, Stats, etc.) ---
@app.get("/statistics")
def get_stats():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM civic_reports").fetchone()[0]
    resolved = conn.execute("SELECT COUNT(*) FROM civic_reports WHERE resolved = 1").fetchone()[0]
    conn.close()
    return {"total_reports": total, "resolved_issues": resolved}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
