import json, random
from utils.status import GameStatus
from models.challenge import Challenge
from models.round import Round
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CHALLENGES_FILE = BASE_DIR / "data" / "challenges.json"

class GameSession:
    def __init__(self, player):
        self.player = player
        self.rounds = []
        self.current_round = None
        self.total_score = 0
        self.challenges = []
        self.status = GameStatus.NOT_STARTED
    
    MAX_ROUNDS = 5 # Maximum number of rounds in a game session

    def load_challenges(self):
        with CHALLENGES_FILE.open('r') as f:
            self.challenges = json.load(f)

    def generate_challenge(self):
        challenge = random.choice(self.challenges)
        self.challenges.remove(challenge)
        return Challenge(
            id=challenge['id'],
            coordinates=tuple(challenge['coordinates']),
            image_path=challenge['imagePath'],
            location_name=challenge.get('locationName')
        )

    def next_round(self):
        if len(self.rounds) < self.MAX_ROUNDS:
            challenge = self.generate_challenge()
            round_number = len(self.rounds) + 1
            self.current_round =  Round(round_number, challenge)
            self.rounds.append(self.current_round)
            self.current_round.start_round()
            if self.current_round.status == GameStatus.COMPLETED:
                self.total_score += self.current_round.score
                self.next_round()
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
        print(f"Game session completed. Total score: {self.total_score:.2f}")
        print(f"Rounds played: {len(self.rounds)}")
        print([f"Round {x.number}: {x.score:.2f}, Distance: {x.distance:.2f} meters" for x in self.rounds])
        self.player.add_game_session(self)