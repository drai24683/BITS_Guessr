class Player:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
        self.games = []  # List of GameSession objects

    def add_game_session(self, gameSession):
        self.games.append(gameSession)
