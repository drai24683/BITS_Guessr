from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models.player import Player
from app.models.game_session import GameSession
from app.utils.status import GameStatus


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static/"), name="static")
templates = Jinja2Templates(directory="app/templates")

game = None


# =========================
# Home
# =========================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# =========================
# Start Game
# =========================

@app.post("/start_game/")
async def start_game(player_name: str = Form(...)):

    global game

    player = Player(player_name)

    game = GameSession(player)

    game.start_game()

    return RedirectResponse(
        url="/game",
        status_code=303
    )


@app.get("/game", response_class=HTMLResponse)
async def show_game(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="game.html",
        context={
            "game": game
        }
    )


# =========================
# Submit Guess
# =========================

@app.post("/round_result/")
async def round_result(
    lat: float = Form(...),
    lng: float = Form(...)
):

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


@app.get("/round_result/", response_class=HTMLResponse)
async def show_round_result(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="round-result.html",
        context={
            "game": game
        }
    )


# =========================
# Next Round
# =========================

@app.post("/next_round/")
async def next_round():

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


@app.get("/game_result/", response_class=HTMLResponse)
async def show_game_result(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="game-result.html",
        context={
            "game": game
        }
    )