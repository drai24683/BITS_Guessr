from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.models.player import Player
from app.models.game_session import GameSession
from app.utils.status import GameStatus


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="./frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html'
    )

game = None  # Global variable to hold the current game session

@app.post("/start_game/", response_class=HTMLResponse)
async def start_game(request: Request, player_name: str = Form(...)):
    player = Player(player_name)
    temp_game = GameSession(player)
    global game
    game = temp_game  # Assign the new game session to the global variable
    game.start_game()
    return templates.TemplateResponse(
        request=request,
        name='game.html',
        context={
            "game":game
        }
    )

@app.post("/round_result/", response_class=HTMLResponse)
async def round_result(request: Request, guess: str = Form(...)):
    lat, lon = map(float, guess.split(','))
    game.submit_guess(lat,lon)
    if game.current_round.status == GameStatus.COMPLETED:
        return templates.TemplateResponse(
            request=request,
            name='round-result.html',
            context={
                 "game":game
            }
        )

@app.post("/next_round")
async def next_round(request: Request):
    game.next_round()
    if game.status == GameStatus.COMPLETED:
        return templates.TemplateResponse(
            request=request,
            name='game-result.html',
            context={
                "game":game
            }
        )
    else:
        return templates.TemplateResponse(
            request=request,
            name='game.html',
            context={
                "game":game
            }
        )
