import json
from pathlib import Path
from random import choice

BASE_DIR = Path(__file__).resolve().parent
CHALLENGES_FILE = BASE_DIR / "app" / "data" / "challenges.json"


def load_challenges():
    with CHALLENGES_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_challenges(challenges):
    with CHALLENGES_FILE.open("w", encoding="utf-8") as f:
        json.dump(challenges, f, ensure_ascii=False, indent=4)
        f.write("\n")


def remove_challenge():
    challenges = load_challenges()
    challenge_id = int(input("id to remove: ").strip())
    remaining = [c for c in challenges if c.get("id") != challenge_id]

    
    if len(remaining) == len(challenges):
        print(f"No challenge found with id={challenge_id}.")
        return None

    save_challenges(remaining)
    print(f"Removed challenge with id={challenge_id}.")
    return challenge_id


def add_challenge():
    challenges = load_challenges()

    challenge_id = int(input("id: ").strip())
    location_name = input("locationName: ").strip()
    coordinates_input = input("coordinates (comma-separated): ").strip()
    coordinates = [float(value.strip()) for value in coordinates_input.split(",") if value.strip()]
    owner = str("Duck")

    new_challenge = {
        "id": challenge_id,
        "imagePath": f"/static/images/challenges/{challenge_id}.jpeg",
        "locationName": location_name,
        "coordinates": coordinates,
        "owner": owner,
    }

    challenges.append(new_challenge)

    save_challenges(challenges)

    print("Appended new challenge:", new_challenge)
    return


while True:
    ch = int(input("enter choice: "))
    if ch == 1:
        add_challenge()
    elif ch == 2:
        remove_challenge()