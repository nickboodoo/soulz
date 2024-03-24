class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}
        self.node_probabilities = {}

    def add_node(self, value, probability=None):
        self.nodes.add(value)
        if probability is not None:
            # Assign a probability score to each node
            self.node_probabilities[value] = probability

    def add_edge(self, from_node, to_node):
        if from_node in self.node_probabilities and to_node in self.node_probabilities:
            # Calculate edge weight as the average of the nodes' probabilities
            distance = (self.node_probabilities[from_node] + self.node_probabilities[to_node]) / 2
        else:
            # Default distance if probabilities are not defined
            distance = 1
        
        self.edges.setdefault(from_node, []).append(to_node)
        self.edges.setdefault(to_node, []).append(from_node)  # Assuming undirected graph
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance

    def generate_graph(self, node_list, edge_list):
        # Nodes are now passed with their probability scores
        for node, probability in node_list:
            self.add_node(node, probability)
        for from_node, to_node in edge_list:
            self.add_edge(from_node, to_node)

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

        for edge in graph.edges[min_node]:
            weight = current_weight + graph.distances[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path

class MapGeneration:
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.current_location = start
        self.goal = goal
        self.game_over = False

    def play(self):
        print(f"Go from {self.current_location} to {self.goal}.")

        while not self.game_over:
            self.display_options()
            choice = input("Where would you like to go? ")
            self.move_player(choice.upper())
            self.check_win_condition()

    def display_options(self):
        _, path = dijkstra(self.graph, self.current_location)
        print(f"\nYou are currently at {self.current_location}.")
        print("Possible destinations and their encounter risks from here:")
        for destination in self.graph.edges[self.current_location]:
            probability = self.graph.distances[(self.current_location, destination)]
            risk_level = self.probability_to_risk_level(probability)
            print(f"  {destination}: {risk_level}")

        if self.goal in path:
            print(f"\nDebugging: Easiest path to {self.goal} is through {path[self.goal]}.\n")
        else:
            print("\nNo direct path to goal. Explore the graph!\n")

    def probability_to_risk_level(self, probability):
        # Convert probability to a qualitative risk level
        if probability < 0.4:
            return "Low risk"
        elif probability < 0.7:
            return "Medium risk"
        else:
            return "High risk"

    def move_player(self, new_location):
        if new_location in self.graph.nodes and new_location in self.graph.edges[self.current_location]:
            self.current_location = new_location
            print(f"\nYou have moved to {new_location}.\n")
        else:
            print("\nInvalid move. Please try again.\n")

    def check_win_condition(self):
        if self.current_location == self.goal:
            print(f"Congratulations! You've reached {self.goal} and won the game!")
            self.game_over = True

node_probabilities = [("A", 0.7), ("B", 0.4), ("C", 0.9), ("D", 0.5)]
# Edges are defined without weights, as weights will be calculated
edges = [("A", "B"), ("B", "C"), ("A", "C"), ("C", "D")]

graph = Graph()
graph.generate_graph(node_probabilities, edges)

# Initializing and starting the game
game = MapGeneration(graph, "A", "D")
game.play()
