import json, random
from app.utils.status import GameStatus
from app.models.challenge import Challenge
from app.models.round import Round
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CHALLENGES_FILE = BASE_DIR / "data" / "challenges.json"

class GameSession:
    MAX_ROUNDS = 5 
    def __init__(self, player):
        self.player = player
        self.rounds = []
        self.current_round = None
        self.total_score = 0
        self.challenges = []
        self.status = GameStatus.NOT_STARTED
    
    def load_challenges(self):
        with CHALLENGES_FILE.open("r", encoding="utf-8") as f:
            self.challenges = json.load(f)

    def generate_challenge(self):
        challenge = random.choice(self.challenges)
        self.challenges.remove(challenge)
        return Challenge(
            id=challenge['id'],
            coordinates=tuple(challenge['coordinates']),
            image_path=challenge['imagePath'],
            location_name=challenge.get('locationName'),
            owner=challenge.get('owner')
        )

    def submit_guess(self, lat, lng):
        if self.current_round.status == GameStatus.COMPLETED:
            return
        self.current_round.submit_guess(lat, lng)
        self.current_round.end_round()
        self.total_score = sum(round.score for round in self.rounds)

    def next_round(self):
        if len(self.rounds) < self.MAX_ROUNDS:
            challenge = self.generate_challenge()
            round_number = len(self.rounds) + 1
            self.current_round = Round(round_number, challenge)
            self.rounds.append(self.current_round)
            self.current_round.start_round()
        else:
            self.end_game()

    def start_game(self):
        if self.status != GameStatus.NOT_STARTED:
            return
        self.load_challenges()
        self.status = GameStatus.ACTIVE
        self.next_round()

    def end_game(self):
        self.status = GameStatus.COMPLETED
        self.player.add_game_session(self)