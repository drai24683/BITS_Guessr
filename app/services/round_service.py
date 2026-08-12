from app.models.challenge import Challenge
from app.models.round import Round
from app.services.database import supabase
from app.utils.status import GameStatus

async def create_round(game_id, round: Round):
    try:
        response = (
            supabase
            .table("rounds")
            .insert({
                "game_id": game_id,
                "round_number": round.number,
                "challenge_id": round.challenge.id,
                "active": True
            })
            .execute()
        )

        round.id = response.data[0]["id"]

        print(
            f"Round {round.number} created "
            f"with round_id: {round.id} "
            f"for game_id: {game_id}"
        )

        return round

    except Exception as e:
        raise RuntimeError(
            f"Failed to create round: {e}"
        ) from e


async def update_round(round: Round):

    active = round.status == GameStatus.ACTIVE

    try:
        supabase.table("rounds").update({
            "guess_lat": round.guess[0] if round.guess else None,
            "guess_lng": round.guess[1] if round.guess else None,
            "score": round.score,
            "distance": round.distance,
            "active": active,
            "started_at": round.started_at.isoformat(),
            "completed_at": (
                round.completed_at.isoformat()
                if round.completed_at is not None
                else None
            )
        }).eq("id", round.id).execute()

        print(
            f"Round {round.number} "
            f"with round_id: {round.id} updated"
        )

        return round

    except Exception as e:
        raise RuntimeError(
            f"Failed to update round: {e}"
        ) from e


async def load_rounds(game_id):

    try:
        response = (
            supabase
            .table("rounds")
            .select("*, challenges(*)")
            .eq("game_id", game_id)
            .order("round_number")
            .execute()
        )

        rounds = []

        for data in response.data:

            challenge_data = data["challenges"]

            challenge = Challenge(
                id=challenge_data["id"],
                coordinates=(
                    challenge_data["latitude"],
                    challenge_data["longitude"]
                ),
                image_path=challenge_data["image_path"],
                location_name=challenge_data.get("location_name"),
                owner=challenge_data.get("owner")
            )

            round = Round(
                number=data["round_number"],
                challenge=challenge
            )

            round.id = data["id"]
            round.score = data["score"] or 0
            round.distance = data["distance"] or 0

            if (
                data["guess_lat"] is not None
                and data["guess_lng"] is not None
            ):
                round.guess = (
                    data["guess_lat"],
                    data["guess_lng"]
                )

            round.status = (
                GameStatus.ACTIVE
                if data["active"]
                else GameStatus.COMPLETED
            )

            rounds.append(round)

        print(
            f"Rounds for game_id: {game_id} "
            f"fetched from database"
        )

        return rounds

    except Exception as e:
        raise RuntimeError(
            f"Failed to load rounds: {e}"
        ) from e