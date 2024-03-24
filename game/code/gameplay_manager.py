from code.initializers.utils import dijkstra

# THIS IS WHERE I NEED TO ADD OLD GAME DATA

class GameplayManager:
    def __init__(self, graph, start, goal, player):
        self.graph = graph
        self.current_location = start
        self.goal = goal
        self.player = player
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