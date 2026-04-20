# IPL 2026 Winner Prediction Engine™ 🏆
### Real-Time AI Forecasting & Analytics Dashboard

**Live Demo:** [https://realtime-ipl-2026-winner-prediction.vercel.app/](https://realtime-ipl-2026-winner-prediction.vercel.app/)

---

## 🚀 Overview
The **IPL 2026 Winner Prediction Engine** is a high-performance analytics platform designed to forecast the outcomes of the 2026 Indian Premier League. Synchronized with **Live 2026 Season Standings**, it provides dynamic probability shifts and championship projections using advanced machine learning.

## 🧠 Technical Architecture
- **Backend:** Flask (Python) running on Vercel Serverless Functions.
- **Frontend:** Premium Landing Page with CSS 3D Glassmorphism and Responsive Design.
- **AI Model:** Random Forest Classifier trained on 18 seasons of IPL data (2008-2025).
- **Update Logic:** Real-time synchronization via the `/api/data` endpoint for daily refreshes.

## ✨ Key Features
- **Live Leaderboard:** Real-time top 5 contenders based on 2026 performance.
- **3D Interactive Cards:** Mouse-responsive tilt effects for an immersive experience.
- **The Challengers:** Survival math for mid-bracket teams.
- **Championship Verdict:** Final AI proclamation of the projected 2026 winner.

## 🛠️ Local Setup
1. **Clone the repository.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the Engine:**
   ```bash
   python api/index.py
   ```
4. **Access the Dashboard:**
   Navigate to `http://127.0.0.1:5000`

## 🌍 Deployment
This project is configured for **Vercel** via the `api/` folder structure and `vercel.json` routing. It also supports **Render/Heroku** via the provided `Procfile`.

---
**Developed by [RAM DHOTE](https://github.com/ramdhote05)**  
*© 2026 IPL Winner Prediction Engine™ • All Rights Reserved*
