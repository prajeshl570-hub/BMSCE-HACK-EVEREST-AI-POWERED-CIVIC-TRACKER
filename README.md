# BMSCE-HACK-EVEREST-AI-POWERED-CIVIC-TRACKER
## 📌 Project Overview
**Theme:** Theme B: AI-Powered Civic Tracker  
**Goal:** A web-based heatmap platform that uses AI to detect potholes/garbage and PostGIS to prevent duplicate reporting.

## 👥 Team Members & USNs
1: (Team Lead)	Prajesh.L	1BM25MC066	prajeshl.mca25@bmsce.ac.in
2: Vishwa Moorthy.S	1BM25MC110	vishwamoorthy.mca25@bmsce.ac.in
3: Prashant Kumar Thakur	1BM25MC114	prashantkumar.mca25@bmsce.ac.in
4: Piyush Kumar	1BM25MC065	Piyushkumar.mca25@bmsce.ac.in
5: Vittal Satteppa Kempasatti	1BM25MC111	vittalsatteppa.mca25@bmsce.ac.in
6: S P Vijayraj	1BM25MC076	spvijayraj.mca25@bmsce.ac.in
7: Rishon raymond Barnes	1BM25MC074	rishonraymond.mca25@bmsce.ac.in
8: Sarvasetty Varshitha 	1BM25MC081 	srvasetty.mca25@bmsce.ac.in

## 🛠️ Tech Stack
* **Frontend:** HTML5, CSS3, JavaScript (Leaflet.js for Heatmaps)
* **Backend:** Python (FastAPI/Flask)
* **AI Model:** YOLOv8 (PyTorch)
* **Database:** PostgreSQL with PostGIS

## 🚀 Features
- **Real-time AI Detection:** Automated validation of civic issues via uploaded photos.
- **Geospatial De-duplication:** Prevents multiple reports for the same location using PostGIS.
- **Dynamic Heatmap:** Visualizes "hot zones" of civic neglect for city authorities.

## ⚙️ Installation & Setup
1. Clone the repo: `git clone [URL]`
2. Install Python deps: `python -m pip install -r requirements.txt`
3. Run the backend with Uvicorn: `python -m uvicorn backend.main:app --reload`
4. Model setup in temp_modal/readme.md 

> Note: `backend/main.py` now exposes a FastAPI app object at `app` so Uvicorn can load it correctly.
