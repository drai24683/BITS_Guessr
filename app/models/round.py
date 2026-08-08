from math import cos, log, pi
from app.models.guess import Guess
from app.utils.status import GameStatus

class Round:
    MAX_SCORE = 5000
    MAX_DISTANCE = 1500
    def __init__(self, number, challenge):
        self.number = number
        self.score = 0
        self.distance = 0
        self.challenge = challenge
        self.guess = None
        self.status = GameStatus.NOT_STARTED

    def submit_guess(self, lat, lng):
        self.guess = Guess(lat, lng)
    
    def calculate_distance(self):
        guess_lat, guess_lng = self.guess.coordinates
        challenge_lat, challenge_lng = self.challenge.coordinates
        delta_lat, delta_lng = ((guess_lat - challenge_lat)*pi/180, (guess_lng - challenge_lng)*cos(challenge_lat*pi/180)*pi/180)
        self.distance = float(f"{((delta_lat**2 + delta_lng**2)**0.5)*6371000:.2f}")
        return self.distance
    def calculate_score (self):
        score_distance = max(0,self.distance-20)
        ratio = score_distance/self.MAX_DISTANCE
        if score_distance <= 750:
            self.score = int(self.MAX_SCORE * (1 - ratio) ** 2.5)
        elif score_distance <= 1000:
            score_at_750 = self.MAX_SCORE * (1 - 750 / 1500) ** 2.5
            t = (score_distance - 750) / 250 
            self.score = int(score_at_750 * (1 - t) ** 2.5)
        return self.score
    def start_round(self):
        self.status = GameStatus.ACTIVE
    def end_round(self):
        if self.guess is None:
            raise ValueError("No guess has been submitted.")
        self.calculate_distance()
        self.calculate_score()
        self.status = GameStatus.COMPLETED