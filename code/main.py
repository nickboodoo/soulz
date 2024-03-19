from game.sequence_loops.world_states import WorldStates
from game.sequence_loops.game_loop import GameLoop
from game.characters.player import Player


if __name__ == "__main__":

    world_state = WorldStates()


    player_name = input("Enter your name: ")
    player = Player(player_name)


    game_loop = GameLoop(player, world_state)


    game_loop.start_loop()