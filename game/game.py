from game.gameloop import GameLoop
from .player import Player
from .messages import welcome_messages

class Game:
    def __init__(self):
        pass

    def start(self):
        player_name = input("Enter your name: ")
        welcome_messages(player_name)

        player = Player(player_name)
        game_loop = GameLoop(player)
        game_loop.start_loop()
