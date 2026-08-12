# BITSGuessr

*A GeoGuessr-inspired web application built for the BITS Pilani Goa campus.*

BITSGuessr challenges players to identify locations around the BITS Goa campus from real photographs. Place a marker on the interactive campus map, submit your guess, and earn points based on how close you are to the actual location.

> **Version:** v1.0.0

---

## Live Demo

🌐 [https://bits-guessr.onrender.com](https://bits-guessr.onrender.com)

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
- 👤 Google OAuth authentication through Supabase Auth
- 🪪 Registered user accounts with usernames and display names
- 👤 User-specific game persistence
- 💾 Completed guest games and rounds persisted to Supabase PostgreSQL
- 🔐 User and guest gameplay handled through the same game system
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

### Authentication & Data

- Supabase Auth
- Google OAuth
- Supabase PostgreSQL
- Supabase Storage
- Google Sheets
- Google Apps Script


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

## How It Works

Challenge submissions are maintained through a Google Sheet and exposed through a Google Apps Script web endpoint.

The application uses Supabase as the persistent source of truth for challenge metadata. Challenge images are stored separately in Supabase Storage.

When a new game starts, the backend queries Supabase for the currently available challenges. Each game receives its own copy of the challenge list, so changes to the challenge database do not affect games that are already in progress.

Registered users authenticate through Google OAuth using Supabase Auth. Once authenticated, users can create persistent games associated with their account.

Guest game state is kept in the server's runtime cache while the game is in progress. Guest games are not written to the database during normal gameplay. Once a guest game is completed, the game and its rounds are persisted to Supabase PostgreSQL.

The `active` field determines whether a challenge is available for new games. Inactive challenges remain in the database so that challenge IDs remain stable and existing references are not affected.

```text
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
             │
       ┌─────┴─────┐
       │           │
   Registered     Guest
      User        Player
       │           │
       ▼           ▼
   Supabase     Runtime
   PostgreSQL     Cache
       │           │
       │       Game Completed
       │           │
       │           ▼
       │       Supabase DB
       │
       ▼
   Persistent Game
```

---

## Authentication

BITSGuessr uses Google OAuth through Supabase Auth for registered accounts.

The authentication flow is:

```text
User
 │
 ▼
BITSGuessr Login
 │
 ▼
Supabase Auth
 │
 ▼
Google OAuth
 │
 ▼
Supabase Auth Callback
 │
 ▼
BITSGuessr /auth/callback
 │
 ├── Existing User
 │       │
 │       ▼
 │     /home
 │
 └── New User
         │
         ▼
    /finish_oauth
         │
         ▼
   Username + Display Name
         │
         ▼
       /home
```

Usernames are unique. If a username is already taken during account setup, the user is returned to the account setup page with an appropriate error message.

Authentication state is maintained through the user's access token, while application-specific account information is stored in the `users` table.

---

## Game Persistence

BITSGuessr uses different persistence strategies for registered users and guests.

### Registered Users

Registered users have their games persisted from the beginning of gameplay.

Game and round state is updated in Supabase as gameplay progresses.

This allows registered users' completed and in-progress game information to be persisted independently of the runtime session.

### Guests

Guest games are kept in the server's runtime cache while they are being played.

Each browser receives a `session_id` cookie which is used to associate the browser with its active `GameSession`.

Guest games are intentionally not written to the database while they are in progress. This prevents abandoned guest games from creating incomplete database records.

Once a guest game is completed, the application creates the game record and its round records in Supabase, then stores the final guesses, scores, distances, and game status.

Database-generated IDs are assigned to games and rounds when they are persisted. Runtime game state does not depend on a database ID until persistence occurs.

---

## Challenge Data Pipeline

New challenges follow this general workflow:

```text
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


### Environment Variables

The application requires access to the Supabase project.

Configure the required Supabase project URL and API credentials through environment variables rather than committing them to the repository.

OAuth configuration also requires the appropriate Google OAuth credentials and Supabase Auth configuration for the deployment environment.

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
│   │   ├── round.py
│   │   └── user.py
│   │
│   ├── scripts/
│   │   ├── migrate_challenges.py
│   │   └── migrate_images.py
│   │
│   ├── services/
│   │   ├── challenge_service.py
│   │   ├── database.py
│   │   ├── game_service.py
│   │   ├── round_service.py
│   │   └── user_service.py
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

BITSGuessr uses Supabase PostgreSQL for persistent application data.

The database contains the following core tables:

### `users`

Stores registered player accounts, including usernames, display names, and account information associated with authenticated users.

### `games`

Stores games associated with registered players, including game status, score, progress, and completion information.

Completed guest games are also stored in this table.

### `rounds`

Stores individual rounds belonging to games, including guesses, scores, distances, and challenges.

### `challenges`

Stores challenge metadata and references to images hosted in Supabase Storage.

The database schema is designed to support persistent games, player statistics, authentication, and leaderboards as these features are implemented.

---

## Roadmap

### Phase 2 — Persistence

- [x] Persistent challenge storage
- [x] Persistent completed guest games
- [x] Persistent guest rounds
- [x] Persist authenticated user games during gameplay
- [ ] Resume active user games after server restart
- [ ] Player statistics
- [ ] Recent games
- [ ] Improved scoring algorithm

### Phase 3 — Accounts & Community

- [x] User authentication
- [x] Registered users
- [x] Guest gameplay
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

- Active game sessions are currently stored in server memory.
- Guest game progress is lost if the server restarts before the game is completed.
- Active authenticated game state depends on the current server session for gameplay continuity.
- Active user games cannot currently be resumed after a server restart.
- Leaderboards and player statistics are not yet available.
- Multiplayer gameplay is not yet implemented.

---

## Author

**Divyanshu Rai**