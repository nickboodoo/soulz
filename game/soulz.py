from code.initializers.game_setup import GameSetup
from code.characters.player import Player

# RUNS CODE

if __name__ == "__main__":

    node_difficulties = [("A", 0.7), ("B", 0.4), ("C", 0.9), ("D", 0.5), ("E", 0.8), ("F", 0.6)]

    player_name = input("Enter your name: ")
    player = Player(player_name)

    setup = GameSetup(node_difficulties, "A", "D", player)
    setup.setup_game()
    setup.initiate_gameplay_loop()

