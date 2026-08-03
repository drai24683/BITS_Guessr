# BitsGuessr 
# GeoGuessr - BITS Pilani version

A GeoGuessr-inspired web application built for the BITS Pilani Goa campus where players identify campus locations from images and place their guesses on an interactive map.

## Features

- 🎮 Multi-round gameplay
- 🗺️ Interactive Leaflet.js map
- 📍 Click-to-place location guessing
- 📏 Distance-based scoring
- 📸 Real campus location challenges
- 🧩 Modular object-oriented backend
- 🎨 Server-side rendering with Jinja2

## Tech Stack

- Python
- FastAPI
- Jinja2
- HTML/CSS
- JavaScript
- Leaflet.js
- OpenStreetMap

## Installation

```bash
git clone https://github.com/yourusername/BITSGuessr.git
cd BITSGuessr

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Visit:

```
http://127.0.0.1:8000
```

## Project Structure

```
app/
├── models/
├── data/
├── static/
├── utils/
└── main.py

frontend/
└── templates/
```

## Roadmap

- [ ] Reveal correct location after each round
- [ ] Display both guess and actual location on the map
- [ ] Timer mode
- [ ] Leaderboard
- [ ] Responsive UI
- [ ] Multiplayer support

## Screenshots

*Coming soon.*

## Author

Divyanshu Rai