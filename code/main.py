
from code.game.game_loop import GameLoop
from game.characters.player import Player


if __name__ == "__main__":


    player_name = input("Enter your name: ")
    player = Player(player_name)


    game_loop = GameLoop(player, world_state)


    game_loop.start_loop()