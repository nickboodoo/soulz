from maps.dynamic_world_map import DynamicWorldMap
from utility.utils import clear_screen
from characters.player import Player
from managers.gameplay_manager import GameplayManager

"""Initializes game settings, including creating the game world and the player character."""

class GameSetup:
    def __init__(self):
        self.node_difficulties = []
        self.start_node = None
        self.end_node = None
        self.graph = None
        self.game = None
        self.player = None

    def initialize_game_settings(self, start_node, end_node):
        self.node_difficulties = [("A", 0.7), ("B", 0.4), ("C", 0.9), ("D", 0.5), ("E", 0.8), ("F", 0.6)]

        self.start_node = start_node
        self.end_node = end_node

    def initialize_player(self):
        # Check for God Mode at the start
        god_mode_input = input("Welcome to Soulz! ")
        god_mode_enabled = god_mode_input.lower() == "tgm"

        player_name = input("Enter your name: ")
        self.player = Player(player_name, god_mode=god_mode_enabled)  # Use the god_mode parameter
        
        clear_screen()

    def setup_game(self):
        self.graph = DynamicWorldMap()
        self.graph.generate_graph(self.node_difficulties)
        self.game = GameplayManager(self.graph, self.start_node, self.end_node, self.player)

    def initiate_gameplay_loop(self):
        if self.game:
            self.game.initiate_gameplay_loop()
        else:
            print("Game not set up. Call setup_game first.")
