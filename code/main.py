from game.game_loop import GameLoop

from game.player import Player

from game.world_states import WorldStates


if __name__ == "__main__":
    world_state = WorldStates()
    player_name = input("Enter your name: ")
    player = Player(player_name)
    game_loop = GameLoop(player, world_state)
    game_loop.start_loop()