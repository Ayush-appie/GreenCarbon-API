# GreenCarbon API 🌱⚡

A Machine Learning REST API deployed on AWS that predicts real-time electrical grid strain.

## 🚀 Live Demo
**Endpoint:** `http://13.60.204.93:8000/optimize?window_hours=24`

## 🛠️ Tech Stack
* **Language:** Python 3
* **Machine Learning:** Scikit-Learn, Pandas
* **API Framework:** FastAPI, Uvicorn
* **Cloud Infrastructure:** AWS EC2 (Ubuntu), SSH

## 💻 Setup
1. Clone: `git clone https://github.com/Ayush-appie/GreenCarbon-API.git`
2. Install: `pip install fastapi uvicorn pandas scikit-learn joblib`
3. Run: `python -m uvicorn app:app --host 0.0.0.0 --port 8000`
