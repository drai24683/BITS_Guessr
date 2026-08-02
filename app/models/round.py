from math import cos, pi
from app.models.guess import Guess
from app.utils.status import GameStatus

class Round:
    MAX_SCORE = 5000
    MAX_DISTANCE = 2000
    def __init__(self, number, challenge):
        self.number = number
        self.score = 0
        self.distance = 0
        self.challenge = challenge
        self.guess = None
        self.status = GameStatus.NOT_STARTED

    def submit_guess(self, guess):
        self.guess = Guess(guess[0], guess[1])
    
    def calculate_distance(self):
        guess_lat, guess_lon = self.guess.coordinates
        challenge_lat, challenge_lon = self.challenge.coordinates
        delta_lat, delta_lon = ((guess_lat - challenge_lat)*pi/180, (guess_lon - challenge_lon)*cos(challenge_lat*pi/180)*pi/180)
        self.distance = float(f"{((delta_lat**2 + delta_lon**2)**0.5)*6371000:.2f}")
        return self.distance
    def calculate_score (self):
        self.score = int(max(0,self.MAX_SCORE*(1 - self.distance/self.MAX_DISTANCE)))
        return self.score
    def start_round(self):
        self.status = GameStatus.ACTIVE
    def end_round(self):
        if self.guess is None:
            raise ValueError("No guess has been submitted.")
        self.calculate_distance()
        self.calculate_score()
        self.status = GameStatus.COMPLETED