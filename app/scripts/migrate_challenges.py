from app.services.challenge_service import fetch_challenges
from app.services.database import supabase


async def migrate_data():
    challenges = await fetch_challenges()

    latest_response = (
        supabase
        .table("challenges")
        .select("id")
        .order("id", desc=True)
        .limit(1)
        .execute()
    )

    latest_id = (
        latest_response.data[0]["id"]
        if latest_response.data
        else 0
    )

    print(f"Latest challenge in database: {latest_id}")

    challenges = sorted(
        challenges,
        key=lambda challenge: challenge["id"]
    )

    challenges = [
        challenge
        for challenge in challenges
        if challenge["id"] > latest_id
    ]

    if not challenges:
        print("No new challenges to migrate.")
        return

    rows = []

    for challenge in challenges:
        latitude, longitude = challenge["coordinates"]

        rows.append({
            "image_path": challenge["imagePath"],
            "latitude": latitude,
            "longitude": longitude,
            "location_name": challenge.get("locationName") or None,
            "owner": challenge.get("owner") or None,
            "email": challenge.get("email"),
            "active": challenge.get("active", True),
        })

    print(
        f"Prepared {len(rows)} new challenges "
        f"({challenges[0]['id']}–{challenges[-1]['id']})."
    )

    response = (
        supabase
        .table("challenges")
        .insert(rows)
        .execute()
    )

    print(f"Inserted {len(response.data)} challenges.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(migrate_data())