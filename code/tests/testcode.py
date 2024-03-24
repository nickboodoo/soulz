class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges.setdefault(from_node, []).append(to_node)
        self.edges.setdefault(to_node, []).append(from_node)  # Assuming undirected graph
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance  # Assuming undirected graph

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
        print("Possible destinations and their distances from here:")
        for destination in self.graph.edges[self.current_location]:
            distance = self.graph.distances[(self.current_location, destination)]
            print(f"  {destination}: {distance} distance unit(s)")

        if self.goal in path:
            print(f"\nDebugging: Shortest path to {self.goal} is through {path[self.goal]}.\n")
        else:
            print("\nNo direct path to goal. Explore the graph!\n")

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

# Setting up the game graph
graph = Graph()
graph.add_node("A")
graph.add_node("B")
graph.add_node("C")
graph.add_node("D")
graph.add_edge("A", "B", 1)
graph.add_edge("B", "C", 2)
graph.add_edge("A", "C", 4)
graph.add_edge("C", "D", 1)

# Initializing and starting the game
game = MapGeneration(graph, "A", "D")
game.play()
