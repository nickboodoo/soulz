import random

"""Manages the game's world map, including nodes (places) and edges (paths between places),
and the difficulties associated with traveling these paths."""

class DynamicWorldMap:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.difficulties = {}
        self.node_difficulties = {}

    def add_node(self, value, difficulty=None):
        self.nodes.add(value)
        if difficulty is not None:
            self.node_difficulties[value] = difficulty

        self.edges[value] = []

    def add_edge(self, from_node, to_node, interaction_forward="normal", interaction_backward="normal"):
        if from_node in self.nodes and to_node in self.nodes:
            self.edges.setdefault(from_node, []).append((to_node, interaction_forward))
            difficulty = (self.node_difficulties.get(from_node, 1) + self.node_difficulties.get(to_node, 1)) / 2
            self.difficulties[(from_node, to_node)] = difficulty

    def direct_path_exists(self, node_a, node_b):
        return node_b in [edge[0] for edge in self.edges.get(node_a, [])] or \
               node_a in [edge[0] for edge in self.edges.get(node_b, [])]

    def generate_graph(self, node_difficulties):
        if not node_difficulties:
            return
        
        self.add_node(node_difficulties[0][0], node_difficulties[0][1])
        for node, difficulty in node_difficulties[1:]:
            self.add_node(node, difficulty)

        for i in range(1, len(node_difficulties)):
            parent_index = random.randint(0, i-1)
            parent_node = node_difficulties[parent_index][0]
            child_node = node_difficulties[i][0]
            if not self.direct_path_exists(parent_node, child_node):
                self.add_edge(parent_node, child_node, "normal", "normal")

        extra_edges = len(node_difficulties) // 2
        while extra_edges > 0:
            node_a, node_b = random.sample(list(self.nodes), 2)
            if not self.direct_path_exists(node_a, node_b):
                self.add_edge(node_a, node_b, "normal", "normal")
                extra_edges -= 1

# CALCULATES SHORTEST PATH (GOAL)

def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge_info in graph.edges[min_node]:
            edge, _ = edge_info
            weight = current_weight + graph.difficulties[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path