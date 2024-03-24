from code.dynamic_world_map import DynamicWorldMap
from code.gameplay_manager import GameplayManager


if __name__ == "__main__":
    node_difficulties = [("A", 0.7), ("B", 0.4), ("C", 0.9), ("D", 0.5), ("E", 0.8), ("F", 0.6)]
    graph = DynamicWorldMap()
    graph.generate_graph(node_difficulties)

    game = GameplayManager(graph, "A", "D")
    game.initiate_gameplay_loop()
