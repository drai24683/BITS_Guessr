from datetime import UTC, datetime
import random
from app.utils.status import GameStatus
from app.models.challenge import Challenge
from app.models.round import Round

class GameSession:
    MAX_ROUNDS = 5 
    def __init__(self, display_name, user_id = None,  game_id = None):
        self.id = game_id
        self.display_name = display_name
        self.user_id = user_id

        self.rounds = []
        self.current_round = None
        self.total_score = 0
        self.challenges = []
        self.status = GameStatus.NOT_STARTED
        self.started_at = None
        self.completed_at = None

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
        if self.status != GameStatus.ACTIVE:
            raise RuntimeError("Game is not active.")

        if self.current_round is None:
            raise RuntimeError("No active round.")

        if self.current_round.status != GameStatus.ACTIVE:
            raise RuntimeError("Current round is not active.")

        self.current_round.submit_guess(lat, lng)
        self.current_round.end_round()
        self.total_score = sum(round.score for round in self.rounds)

    def next_round(self):
        if self.current_round is not None:
            if self.current_round.status != GameStatus.COMPLETED:
                raise RuntimeError(
                    "Cannot start the next round before completing the current round."
                )
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
        self.status = GameStatus.ACTIVE
        self.started_at = datetime.now(UTC)
        self.next_round()

    def end_game(self):
        self.status = GameStatus.COMPLETED
        self.completed_at = datetime.now(UTC)