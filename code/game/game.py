from game.utils import print_welcome_messages
from game.player import Player
from game.game_loop import GameLoop


class Game:
    def __init__(self):
        pass

    def start(self):

        player_name = input("Enter your name: ")

        print_welcome_messages(player_name)

        player = Player(player_name)
        game_loop = GameLoop(player)
        game_loop.start_loop()