import json
from pathlib import Path
import httpx

CHALLENGES_API_URL = "https://script.google.com/macros/s/AKfycbyiOvzc9zdZABZj6G2wSHJ24wVz4iPN614SadTHE_jtQhxMNq07XC6GVDnpmytHSA8Q/exec"
BASE_DIR = Path(__file__).resolve().parents[1]
CHALLENGES_FILE = BASE_DIR / "data" / "challenges.json"


async def fetch_challenges():
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        response = await client.get(CHALLENGES_API_URL)
        response.raise_for_status()
        return response.json()


def load_local_challenges():
    with CHALLENGES_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


async def get_available_challenges():
    try:
        return await fetch_challenges()
    except Exception as e:
        print(f"Challenge API unavailable: {e}")
        print("Using local challenge data.")
        return load_local_challenges()