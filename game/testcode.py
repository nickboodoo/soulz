import random

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

class GameplayManager:
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.current_location = start
        self.goal = goal
        self.game_over = False
        self.breadcrumbs = [start]
        

    def initiate_gameplay_loop(self):
        print(f"Go from {self.current_location} to {self.goal}.")

        while not self.game_over:
            self.display_movement_options()
            choice = input("Where would you like to go? ")
            self.move_player(choice.upper())
            self.check_win_condition()

    def display_movement_options(self):
        _, path = dijkstra(self.graph, self.current_location)
        print(f"\nYou are currently at {self.current_location}.")
        
        if self.current_location in self.graph.edges and self.graph.edges[self.current_location]:
            print("Forward paths and their encounter difficulties:")
            for destination, interaction_type in self.graph.edges[self.current_location]:
                difficulty = self.graph.difficulties[(self.current_location, destination)]
                risk_level = self.difficulty_to_risk_level(difficulty)
                print(f"  {destination} ({interaction_type}): {risk_level}")

        if len(self.breadcrumbs) > 1:
            print("\nBacktrack to:")
            print(f"  {self.breadcrumbs[-2]} (Previous location)")
        else:
            print("\nNo paths leading from this location.")

    def difficulty_to_risk_level(self, difficulty):
        if difficulty < 0.4:
            return "Low difficulty"
        elif difficulty < 0.7:
            return "Medium difficulty"
        else:
            return "High difficulty"

    def move_player(self, new_location):
        if new_location in [edge[0] for edge in self.graph.edges.get(self.current_location, [])]:
            self.breadcrumbs.append(new_location)  
            self.current_location = new_location
            print(f"\nYou have moved to {new_location}.\n")
        elif new_location == self.breadcrumbs[-2] if len(self.breadcrumbs) > 1 else None:
            self.breadcrumbs.pop()
            self.current_location = new_location
            print(f"\nYou have moved back to {new_location}.\n")
        else:
            print("\nInvalid move. Please try again.\n")

    def check_win_condition(self):
        if self.current_location == self.goal:
            print(f"Congratulations! You've reached {self.goal} and won the game!")
            self.game_over = True

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



node_difficulties = [("A", 0.7), ("B", 0.4), ("C", 0.9), ("D", 0.5), ("E", 0.8), ("F", 0.6)]
    
setup = GameSetup(node_difficulties, "A", "D")
setup.setup_game()
setup.initiate_gameplay_loop()