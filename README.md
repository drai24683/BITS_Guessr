# BITSGuessr

*A GeoGuessr-inspired web application built for the BITS Pilani Goa campus.*

BITSGuessr challenges players to identify locations around the BITS Goa campus from real photographs. Place a marker on the interactive campus map, submit your guess, and earn points based on how close you are to the actual location.

---

## Features

- 🎮 Five-round gameplay
- 🗺️ Interactive campus map powered by Leaflet.js
- 📍 Click-to-place guessing system
- 📏 Distance-based scoring
- 📊 Live in-game HUD with total score tracking
- 📸 Real BITS Goa campus location challenges
- 📍 Round result maps showing guesses, correct locations, and connecting paths
- 🏁 Interactive final results map summarizing all five rounds
- 🎨 Responsive BITS-inspired user interface
- 🧩 Modular object-oriented backend
- 🖥️ Server-side rendering using FastAPI and Jinja2

---

## Tech Stack

### Backend

- Python
- FastAPI
- Jinja2

### Frontend

- HTML5
- CSS3
- JavaScript
- Leaflet.js
- OpenStreetMap

---

## Installation

```bash
git clone https://github.com/yourusername/BITSGuessr.git
cd BITSGuessr

python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Open your browser and visit:

```
http://127.0.0.1:8000
```

---

## Project Structure

```
BITSGuessr/
│
├── app/
│   ├── data/
│   ├── models/
│   ├── routes/
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   └── js/
│   ├── templates/
│   ├── utils/
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

## Roadmap

### Phase 2 — Web Application

- [ ] Session-based gameplay (multiple simultaneous users)
- [ ] Persistent game storage
- [ ] SQLite/PostgreSQL integration
- [ ] Deployment

### Future Features

- [ ] Timer mode
- [ ] Recent games page
- [ ] Campus leaderboard
- [ ] User authentication
- [ ] Community challenge submission
- [ ] Multiplayer mode
- [ ] React frontend (optional)

---

## Author

**Divyanshu Rai**