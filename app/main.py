from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid

from app.models.user import User
from app.models.game_session import GameSession
from app.services.auth_service import (
    create_pkce_challenge,
    create_pkce_verifier,
    get_current_user,
    get_google_login_url,
    exchange_code,
)
from app.services.challenge_service import get_available_challenges
from app.services.game_service import create_game, update_game
from app.services.round_service import create_round, update_round
from app.services.user_service import load_user, create_user
from app.utils.status import GameStatus


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/templates"
)

games = {}  # {session_id: GameSession}


# =========================
# Runtime Game Helpers
# =========================

def get_game(request: Request) -> GameSession | None:

    session_id = request.cookies.get("session_id")

    if session_id is None:
        return None

    return games.get(session_id)


def store_game(
    request: Request,
    game: GameSession
):
    session_id = request.cookies.get("session_id")

    if session_id is None:
        raise ValueError("No session_id cookie.")

    games[session_id] = game


# =========================
# Favicon
# =========================

@app.get(
    "/favicon.ico",
    include_in_schema=False
)
async def favicon() -> FileResponse:

    return FileResponse(
        "app/static/images/favicon.png"
    )


# =========================
# Home
# =========================

@app.get("/",response_class=HTMLResponse)
async def index(request: Request):

    session_id = request.cookies.get(
        "session_id"
    )

    if session_id is None:
        session_id = str(uuid.uuid4())

    auth_user = get_current_user(request)

    user = None

    if auth_user is not None:
        user = await load_user(
            auth_user.id
        )

    response = templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": user
        }
    )

    response.set_cookie(
        key="session_id",
        value=session_id
    )

    return response

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):

    session_id = request.cookies.get("session_id")

    if session_id is None:
        session_id = str(uuid.uuid4())


    user_id = get_current_user(request).id
    user = await load_user(user_id)

    response = templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "user": user,
        }
    )
    return response


# =========================
# Authentication
# =========================

@app.get("/login")
async def login(request: Request):

    code_verifier = create_pkce_verifier()

    code_challenge = create_pkce_challenge(
        code_verifier
    )

    redirect_to = str(
        request.url_for("auth_callback")
    )

    login_url = get_google_login_url(
        redirect_to,
        code_challenge
    )

    response = RedirectResponse(
        login_url
    )

    response.set_cookie(
        key="auth_code_verifier",
        value=code_verifier,
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=600,
    )

    return response


@app.get("/auth/callback")
async def auth_callback(
    request: Request,
    code: str
):

    code_verifier = request.cookies.get(
        "auth_code_verifier"
    )

    if code_verifier is None:
        raise RuntimeError(
            "Missing PKCE code verifier."
        )

    try:

        auth_response = exchange_code(
            code,
            code_verifier
        )

        session = auth_response.session
        auth_user = auth_response.user

        print(
            "Successfully authenticated!"
        )
        print(
            f"User ID: {auth_user.id}"
        )
        print(
            f"Email: {auth_user.email}"
        )

        existing_user = await load_user(
            auth_user.id
        )

        if existing_user is None:
            redirect_url = "/finish_oauth"
        else:
            redirect_url = "/home"

        response = RedirectResponse(
            redirect_url,
            status_code=303
        )

        response.set_cookie(
            key="access_token",
            value=session.access_token,
            httponly=True,
            secure=False,  # True in production
            samesite="lax",
            max_age=3600
        )

        response.set_cookie(
            key="refresh_token",
            value=session.refresh_token,
            httponly=True,
            secure=False,  # True in production
            samesite="lax",
            max_age=60 * 60 * 24 * 30
        )

        response.delete_cookie(
            "auth_code_verifier"
        )

        return response

    except Exception as e:
        raise RuntimeError(
            f"Authentication failed: {e}"
        ) from e


# =========================
# Finish OAuth
# =========================

@app.get(
    "/finish_oauth",
    response_class=HTMLResponse
)
async def show_finish_oauth(
    request: Request
):

    auth_user = get_current_user(request)

    if auth_user is None:
        return RedirectResponse(
            "/",
            status_code=303
        )

    existing_user = await load_user(
        auth_user.id
    )

    if existing_user is not None:
        return RedirectResponse(
            "/",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="finish-oauth.html"
    )


@app.post("/finish_oauth")
async def finish_oauth(
    request: Request,
    username: str = Form(...),
    display_name: str = Form(...)
):

    auth_user = get_current_user(request)

    if auth_user is None:
        return RedirectResponse(
            "/",
            status_code=303
        )

    try:

        await create_user(
            auth_user.id,
            username,
            display_name,
            auth_user.email
        )

        return RedirectResponse(
            "/",
            status_code=303
        )

    except Exception as e:
        raise RuntimeError(
            f"Failed to finish account setup: {e}"
        ) from e


# =========================
# Start Game
# =========================

@app.post("/start_game")
async def start_game(
    request: Request,
    display_name: str | None = Form(None)
):

    existing_game = get_game(request)

    if existing_game is not None:
        if existing_game.status == GameStatus.ACTIVE:
            return RedirectResponse(
                "/game",
                status_code=303
            )

    auth_user = get_current_user(request)

    user = None

    if auth_user is not None:
        user = await load_user(
            auth_user.id
        )

    challenges = await get_available_challenges()

    if not challenges:
        raise RuntimeError(
            "No challenges available."
        )

    print(
        f"Loaded {len(challenges)} challenges."
    )

    if user is not None:

        game = GameSession(
            user.display_name,
            user_id=user.id
        )

    else:

        if not display_name:
            raise RuntimeError(
                "Guest display name is required."
            )

        game = GameSession(
            display_name
        )

    game.challenges = challenges.copy()

    store_game(
        request,
        game
    )

    game.start_game()

    return RedirectResponse(
        "/game",
        status_code=303
    )


# =========================
# Game
# =========================

@app.get(
    "/game",
    response_class=HTMLResponse
)
async def show_game(request: Request):

    game = get_game(request)

    if game is None:
        return RedirectResponse(
            "/",
            status_code=303
        )

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
        return RedirectResponse(
            "/",
            status_code=303
        )

    if game.current_round is None:
        return RedirectResponse(
            "/",
            status_code=303
        )

    if (
        game.current_round.status
        == GameStatus.COMPLETED
    ):
        return RedirectResponse(
            "/round_result",
            status_code=303
        )

    game.submit_guess(
        lat,
        lng
    )

    if (
        game.current_round.status
        != GameStatus.COMPLETED
    ):
        return HTMLResponse(
            content="Round not completed.",
            status_code=400
        )

    return RedirectResponse(
        "/round_result",
        status_code=303
    )


@app.get(
    "/round_result",
    response_class=HTMLResponse
)
async def show_round_result(
    request: Request
):

    game = get_game(request)

    if game is None:
        return RedirectResponse(
            "/",
            status_code=303
        )

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
        return RedirectResponse(
            "/",
            status_code=303
        )

    if game.status == GameStatus.COMPLETED:
        return RedirectResponse(
            "/game_result",
            status_code=303
        )

    if game.current_round is None:
        return RedirectResponse(
            "/",
            status_code=303
        )

    if (
        game.current_round.status
        != GameStatus.COMPLETED
    ):
        return RedirectResponse(
            "/game",
            status_code=303
        )

    game.next_round()

    if game.status == GameStatus.COMPLETED:
        return RedirectResponse(
            "/game_result",
            status_code=303
        )

    return RedirectResponse(
        "/game",
        status_code=303
    )


# =========================
# Game Result
# =========================

@app.get(
    "/game_result",
    response_class=HTMLResponse
)
async def show_game_result(
    request: Request
):

    game = get_game(request)

    if game is None:
        return RedirectResponse(
            "/",
            status_code=303
        )

    if game.id is None:

        persisted_game = await create_game(
            game.display_name,
            game.user_id
        )

        game.id = persisted_game.id

    for round in game.rounds:

        if round.id is None:
            await create_round(
                game.id,
                round
            )

    rounds_json = []

    for round in game.rounds:

        if round.id is not None:
            await update_round(round)

        rounds_json.append({
            "guess": round.guess,
            "answer": round.challenge.coordinates,
            "score": round.score,
            "distance": round.distance,
        })

    await update_game(game)

    return templates.TemplateResponse(
        request,
        "game-result.html",
        {
            "game": game,
            "rounds_json": rounds_json,
        }
    )