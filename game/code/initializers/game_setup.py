from code.initializers.dynamic_world_map import DynamicWorldMap
from code.gameplay_manager import GameplayManager

# INITIALIZES GAME SETUP BY GENERATING MAP AND CREATING GAME OBJECT FROM GAMEPLAYMANAGER

class GameSetup:
    def __init__(self, node_difficulties, start_node, end_node):
        self.node_difficulties = node_difficulties
        self.start_node = start_node
        self.end_node = end_node
        self.graph = None
        self.game = None

    def setup_game(self):
        self.graph = DynamicWorldMap()
        self.graph.generate_graph(self.node_difficulties)
        self.game = GameplayManager(self.graph, self.start_node, self.end_node)

    def initiate_gameplay_loop(self):
        if self.game:
            self.game.initiate_gameplay_loop()
        else:
            print("Game not set up. Call setup_game first.")
