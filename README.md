# BITSGuessr

*A GeoGuessr-inspired web application built for the BITS Pilani Goa campus.*

BITSGuessr challenges players to identify locations around the BITS Goa campus from real photographs. Place a marker on the interactive campus map, submit your guess, and earn points based on how close you are to the actual location.

> **Version:** v1.0.0

---

## Features

- 🎮 Five-round gameplay
- 🌐 Session-based gameplay supporting multiple simultaneous users
- 🗺️ Interactive campus map powered by Leaflet.js
- 📍 Click-to-place guessing system
- ⌨️ Keyboard controls for map navigation and gameplay
- 📏 Distance-based scoring
- 📊 Live in-game HUD with score tracking
- 📸 Real BITS Goa campus location challenges
- 📍 Round result maps showing guesses, correct locations, and connecting paths
- 🏁 Interactive final results map summarizing all rounds
- ℹ️ In-game help and controls overlay
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
git clone https://github.com/drai24683/BITSGuessr.git
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
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   ├── js/
│   │   └── backgrounds/
│   ├── templates/
│   │   └── partials/
│   ├── utils/
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

## Roadmap

### Phase 2 — Persistence

- [ ] Persistent game storage
- [ ] SQLite database
- [ ] PostgreSQL support
- [ ] Player statistics
- [ ] Recent games page

### Phase 3 — Community

- [ ] Campus leaderboard
- [ ] User authentication
- [ ] Community challenge submission
- [ ] Challenge moderation tools

### Future Ideas

- [ ] Timer mode
- [ ] Multiplayer mode
- [ ] Daily challenge
- [ ] Difficulty settings
- [ ] More campus locations
- [ ] React frontend (optional)

---

## Current Limitations

- Game progress is stored only for the current browser session.
- Completed games are not yet persisted to a database.
- Leaderboards and player statistics are planned for a future release.

---

## Author

**Divyanshu Rai**