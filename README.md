# BITSGuessr

*A GeoGuessr-inspired web application for the BITS Pilani Goa campus.*

Players are shown an image captured somewhere on campus and must identify its location by placing a marker on an interactive map. The closer the guess, the higher the score.

---

## Features

- 🎮 Five-round gameplay
- 🗺️ Interactive campus map using Leaflet.js
- 📍 Click-to-place guessing system
- 📏 Distance-based scoring
- 🏆 End-of-game score summary
- 📸 Real BITS Goa campus location challenges
- 🎨 Responsive UI with a custom BITS-inspired theme
- 🧩 Modular object-oriented backend
- 🖥️ Server-side rendering using Jinja2 templates

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
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   ├── js/
│   │   └── background/
│   ├── templates/
│   ├── utils/
│   └── main.py
│
├── requirements.txt
└── README.md
```

---


## Future Plans

- [ ] Reveal the correct location after every round
- [ ] Show both guessed and actual locations on the map
- [ ] Draw a line between the guess and the correct location
- [ ] Timer mode
- [ ] Persistent leaderboard
- [ ] User authentication
- [ ] Multiplayer mode
- [ ] React frontend
- [ ] Database support (SQLite/PostgreSQL)
- [ ] Deployment

---

## Author

**Divyanshu Rai**