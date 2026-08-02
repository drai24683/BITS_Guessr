from models.player import Player
from models.game_session import GameSession

game = GameSession(Player("Alice"))

game.start_game()