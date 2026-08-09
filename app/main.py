from contextlib import asynccontextmanager
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid

from app.models.player import Player
from app.models.game_session import GameSession
from app.services.challenge_service import get_available_challenges
from app.utils.status import GameStatus


challenges_cache = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    global challenges_cache

    challenges_cache = await get_available_challenges()

    if not challenges_cache:
        raise RuntimeError("No challenges available.")

    print(f"Loaded {len(challenges_cache)} challenges.")

    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

games = {}          # multi browser persistence { session_id : game }

def get_game(request: Request) -> GameSession | None:

    session_id = request.cookies.get("session_id")

    if session_id is None:
        return None

    return games.get(session_id)

def store_game(request: Request, game: GameSession):

    session_id = request.cookies.get("session_id")

    if session_id is None:
        raise ValueError("No session_id cookie.")

    games[session_id] = game

@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse("app/static/images/favicon.png")


# =========================
# Home
# =========================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    session_id = request.cookies.get("session_id")

    if session_id is None:
        session_id = str(uuid.uuid4())

    response = templates.TemplateResponse(
        request=request,
        name="index.html"
    )

    response.set_cookie(
        key="session_id",
        value=session_id
    )

    return response

    


# =========================
# Start Game
# =========================

@app.post("/start_game")
async def start_game(request: Request, player_name: str = Form(...)):

    existing_game = get_game(request)

    if existing_game is not None:
        return RedirectResponse(
            url="/game",
            status_code=303
        )

    game = GameSession(Player(player_name))
    game.challenges = challenges_cache.copy()

    store_game(request, game)

    game.start_game()

    return RedirectResponse(
        url="/game",
        status_code=303
    )

@app.get("/game", response_class=HTMLResponse)
async def show_game(request: Request):

    game = get_game(request)

    if game is None:
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="game.html",
        context={
            "game": game,
            "show_header": False
        }
    )


# =========================
# Submit Guess
# =========================

@app.post("/round_result")
async def round_result(
    request: Request, 
    lat: float = Form(...),
    lng: float = Form(...)
):
    game = get_game(request)

    if game is None:
        return RedirectResponse("/", status_code=303)

    if game.current_round is None:
        return RedirectResponse("/", status_code=303)

    if game.current_round.status == GameStatus.COMPLETED:
        return RedirectResponse(
            url="/round_result",
            status_code=303
        )

    game.submit_guess(lat, lng)

    if game.current_round.status != GameStatus.COMPLETED:

        return HTMLResponse(
            content="Round not completed.",
            status_code=400
        )

    return RedirectResponse(
        url="/round_result",
        status_code=303
    )


@app.get("/round_result", response_class=HTMLResponse)
async def show_round_result(request: Request):

    game = get_game(request)

    if game is None:
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="round-result.html",
        context={
            "game": game,
            "show_header": False
        }
    )


# =========================
# Next Round
# =========================

@app.post("/next_round")
async def next_round(request: Request):

    game = get_game(request)

    if game is None:
        return RedirectResponse("/", status_code=303)

    if game.status == GameStatus.COMPLETED:
        return RedirectResponse(
            url="/game_result",
            status_code=303
        )

    if game.current_round is None:
        return RedirectResponse("/", status_code=303)

    if game.current_round.status != GameStatus.COMPLETED:
        return RedirectResponse(
            url="/game",
            status_code=303
        )

    game.next_round()

    if game.status == GameStatus.COMPLETED:
        return RedirectResponse(
            url="/game_result",
            status_code=303
        )

    return RedirectResponse(
        url="/game",
        status_code=303
    )

@app.get("/game_result", response_class=HTMLResponse)
async def show_game_result(request: Request):

    game = get_game(request)

    if game is None:
        return RedirectResponse("/", status_code=303)

    rounds_json = []

    for round in game.rounds:
        rounds_json.append({
            "guess": round.guess.coordinates,
            "answer": round.challenge.coordinates,
            "score": round.score,
            "distance": round.distance,
        })

    return templates.TemplateResponse(
        request,
        "game-result.html",
        {
            "game": game,
            "rounds_json": rounds_json,
        }
    )