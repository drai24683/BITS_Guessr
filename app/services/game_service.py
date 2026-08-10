from datetime import datetime, timezone

from app.models.game_session import GameSession
from app.services.database import supabase
from app.utils.status import GameStatus


async def create_game(display_name: str, user_id=None):

    try:
        response = (
            supabase
            .table("games")
            .insert({
                "user_id": user_id,
                "display_name": display_name,
                "active": True
            }).execute())

        game_id = response.data[0]["id"]

        game = GameSession(
            display_name,
            game_id,
            user_id
        )

        print(f"Game created with game_id: {game_id}")

        return game

    except Exception as e:
        raise RuntimeError(f"Failed to create game: {e}") from e


async def update_game(game: GameSession):

    active = game.status == GameStatus.ACTIVE

    completed_at = (
        None
        if active
        else datetime.now(timezone.utc).isoformat()
    )

    try:
        supabase.table("games").update({
            "current_round_number": (
                game.current_round.number
                if game.current_round
                else None
            ),
            "total_score": game.total_score,
            "active": active,
            "completed_at": completed_at
        }).eq("id", game.id).execute()

        print(f"Game with game_id: {game.id} updated in Database")

        return game

    except Exception as e:
        raise RuntimeError(
            f"Failed to update game: {e}"
        ) from e


async def load_game(game_id):

    try:
        response = (
            supabase
            .table("games")
            .select("*")
            .eq("id", game_id)
            .single()
            .execute()
        )

        data = response.data

        game = GameSession(
            data["display_name"],
            data["id"],
            data["user_id"]
        )

        game.total_score = data["total_score"]
        game.status = (
            GameStatus.ACTIVE
            if data["active"]
            else GameStatus.COMPLETED
        )

        print(f"Game with game_id: {game_id} fetched from database")

        return game

    except Exception as e:
        raise RuntimeError(
            f"Failed to load game: {e}"
        ) from e