# BITSGuessr

*A GeoGuessr-inspired web application built for the BITS Pilani Goa campus.*

BITSGuessr challenges players to identify locations around the BITS Goa campus from real photographs. Place a marker on the interactive campus map, submit your guess, and earn points based on how close you are to the actual location.

> **Version:** v1.0.0

---

## Live Demo

🌐 https://bitsguessr.onrender.com

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
- 🏁 Interactive final results map summarizing all five rounds
- ℹ️ In-game help, controls, and project information overlay
- 📱 Responsive design for desktop and mobile devices
- 🎨 Custom BITS-inspired user interface
- 🧩 Modular object-oriented backend
- 🔄 Challenge data loaded from an external Google Apps Script API
- 💾 Startup caching of challenge data with local JSON fallback
- 🖥️ Server-side rendering using FastAPI and Jinja2

---

## Tech Stack

### Backend

- Python
- FastAPI
- Jinja2
- HTTPX

### Frontend

- HTML5
- CSS3
- JavaScript
- Leaflet.js
- OpenStreetMap

### Data & Storage

- Google Sheets
- Google Apps Script
- Google Drive
- Local JSON fallback

---

## How It Works

Challenge metadata is maintained through a Google Sheet and exposed through a Google Apps Script web endpoint.

When the application starts, the backend fetches the available challenges and stores them in an in-memory cache. Individual game sessions receive their own copy of the challenge list, allowing challenges to be removed from a game without modifying the global cache.

If the external challenge API is unavailable, BITSGuessr automatically falls back to the local `challenges.json` dataset.

```text
Google Sheets
     │
     ▼
Google Apps Script
     │
     ▼
Challenge Service
     │
     ├── External API
     │
     └── Local JSON fallback
     │
     ▼
Application Cache
     │
     ▼
Game Sessions
```

Images are hosted on Google Drive and referenced by URL from the challenge data.

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

```text
http://127.0.0.1:8000
```

---

## Project Structure

```text
BITSGuessr/
│
├── app/
│   ├── data/
│   │   └── challenges.json
│   │
│   ├── models/
│   │   ├── challenge.py
│   │   ├── game_session.py
│   │   ├── player.py
│   │   └── round.py
│   │
│   ├── services/
│   │   └── challenge_service.py
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   ├── js/
│   │   └── backgrounds/
│   │
│   ├── templates/
│   │   └── partials/
│   │
│   ├── utils/
│   │   └── status.py
│   │
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
- [ ] Recent games
- [ ] Improved scoring algorithm

### Phase 3 — Accounts & Community

- [ ] User authentication
- [ ] Campus leaderboard
- [ ] Player profiles
- [ ] Community challenge submission
- [ ] Challenge moderation tools

### Future Ideas

- [ ] Timer mode
- [ ] Multiplayer mode
- [ ] Daily challenge
- [ ] Difficulty settings
- [ ] More campus locations
- [ ] Analytics dashboard
- [ ] React frontend (optional)

---

## Contributing

Have an interesting campus location that would make a fun challenge?

You can submit suggestions here:

https://forms.gle/U3zFfAHEZJtArEYB9

Bug reports, feature requests, and general feedback are always appreciated.

---

## Current Limitations

- Game sessions are currently stored in server memory.
- Game progress is lost when the server restarts.
- Completed games are not yet persisted to a database.
- User accounts and authentication are not yet implemented.
- Leaderboards and player statistics are not yet available.
- Multiplayer gameplay is not yet implemented.

---

## Author

**Divyanshu Rai**