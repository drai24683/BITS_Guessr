from math import cos, pi
from models.guess import Guess
from utils.status import GameStatus

class Round:
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
        self.distance = ((delta_lat**2 + delta_lon**2)**0.5)*6371000
        return self.distance
    def calculate_score (self):
        self.score = max(0,5000*(1 - self.distance/2000))
        return self.score
    def start_round(self):
        self.status = GameStatus.ACTIVE
        guess = tuple(float(x) for x in input(f"Round {self.number}: Please enter your guess as 'latitude,longitude': ").split(','))
        print(f"Your guess: {guess}")
        self.submit_guess(guess)
        self.end_round()

    def end_round(self):
        if self.guess is None:
            raise ValueError("No guess has been submitted.")
        self.calculate_distance()
        self.calculate_score()
        print(f"Round {self.number} completed. Distance: {self.distance:.2f} meters, Score: {self.score:.2f}")
        self.status = GameStatus.COMPLETED