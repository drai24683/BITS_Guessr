# BITSGuessr

*A GeoGuessr-inspired web application built for the BITS Pilani Goa campus.*

BITSGuessr challenges players to identify locations around the BITS Goa campus from real photographs. Place a marker on the interactive campus map, submit your guess, and earn points based on how close you are to the actual location.

> **Version:** v1.0.0

---

## Live Demo

🌐 [https://bitsguessr.onrender.com](https://bitsguessr.onrender.com)

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
- 🔄 Challenge data synchronized from Google Sheets through Google Apps Script
- 💾 Persistent challenge metadata using Supabase PostgreSQL
- 🖼️ Challenge images hosted using Supabase Storage
- 🔀 Active/inactive challenge management without changing challenge IDs
- 🆕 Fresh challenge data loaded from the database whenever a new game starts
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

- Supabase PostgreSQL
- Supabase Storage
- Google Sheets
- Google Apps Script

---

## How It Works

Challenge submissions are maintained through a Google Sheet and exposed through a Google Apps Script web endpoint.

The application uses Supabase as the persistent source of truth for challenge metadata. Challenge images are stored separately in Supabase Storage.

When a new game starts, the backend queries Supabase for the currently available challenges. Each game receives its own copy of the challenge list, so changes to the challenge database do not affect games that are already in progress.

The `active` field determines whether a challenge is available for new games. Inactive challenges remain in the database so that challenge IDs remain stable and existing references are not affected.

```
Google Sheets
     │
     ▼
Google Apps Script
     │
     ▼
Challenge Migration
     │
     ├───────────────┐
     ▼               ▼
Supabase DB    Supabase Storage
(metadata)         (images)
     │               │
     └───────┬───────┘
             ▼
     Challenge Service
             │
             ▼
        New Game
             │
             ▼
       Game Session
```

---

## Challenge Data Pipeline

New challenges follow this general workflow:

```
Google Form
     │
     ▼
Google Sheets
     │
     ▼
Google Apps Script API
     │
     ▼
Migration Script
     │
     ├── Challenge metadata → Supabase PostgreSQL
     │
     └── Challenge image    → Supabase Storage
```

The migration process supports incremental updates, allowing only challenges that have not yet been migrated to be inserted into the database.

Inactive challenges are still migrated and stored. Their `active` status is used only when determining which challenges are available for new games.

---

## Installation

```
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

### Environment Variables

The application requires access to the Supabase project.

Configure the required Supabase project URL and API credentials through environment variables rather than committing them to the repository.

---

## Project Structure

```
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
│   ├── scripts/
│   │   ├── migrate_challenges.py
│   │   └── migrate_images.py
│   │
│   ├── services/
│   │   ├── challenge_service.py
│   │   └── database.py
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   └── js/
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

## Database

BITSGuessr currently uses Supabase PostgreSQL for persistent challenge data.

The database contains the following core tables:

### `users`

Stores registered player accounts.

### `games`

Stores games associated with players, including game status, score, and progress.

### `rounds`

Stores individual rounds belonging to games, including guesses, scores, distances, and challenges.

### `challenges`

Stores challenge metadata and references to images hosted in Supabase Storage.

The database schema is designed to support persistent games, player statistics, authentication, and leaderboards as these features are implemented.

---

## Roadmap

### Phase 2 — Persistence

- [ ] Persistent game storage
- [ ] Persist individual rounds
- [ ] Resume active games after server restart
- [ ] Player statistics
- [ ] Recent games
- [ ] Improved scoring algorithm

### Phase 3 — Accounts & Community

- [ ] User authentication
- [ ] Registered users
- [ ] Guest gameplay
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

[https://forms.gle/U3zFfAHEZJtArEYB9](https://forms.gle/U3zFfAHEZJtArEYB9)

Bug reports, feature requests, and general feedback are always appreciated.

---

## Current Limitations

- Game sessions are currently stored in server memory.
- Game progress is lost when the server restarts.
- Games and rounds are not yet written to the database during gameplay.
- User accounts and authentication are not yet implemented.
- Leaderboards and player statistics are not yet available.
- Multiplayer gameplay is not yet implemented.

---

## Author

**Divyanshu Rai**