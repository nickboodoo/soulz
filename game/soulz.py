
# RUNS CODE

from game_setup import GameSetup
from player import Player


if __name__ == "__main__":

    setup = GameSetup()
    setup.initialize_game_settings("A", "D")
    setup.setup_game()
    setup.initiate_gameplay_loop()

