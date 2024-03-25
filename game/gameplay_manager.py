import random
from battle_manager import BattleManager
from boss_battle import BossBattle
from enemy import Enemy
from utils import clear_screen, navigate_player_menu
from utils import dijkstra

"""Manages the gameplay loop, allowing the player to navigate through the world, encounter enemies, and progress towards a goal."""

class GameplayManager:
    def __init__(self, graph, start, goal, player):
        self.graph = graph
        self.current_location = start
        self.goal = goal
        self.player = player
        self.game_over = False
        self.breadcrumbs = [start]
        

    def initiate_gameplay_loop(self):
        while not self.game_over and self.player.is_alive():
            self.display_movement_options()
            print("Menu")
            print("Journal")
            print("Hint")
            print("Quit")
            choice = input("Where would you like to go? ")
            clear_screen()

            if choice.lower() == "menu":
                navigate_player_menu(self.player)

            elif choice.lower() == "hint":
                self.suggest_optimal_path()
            
            elif choice.lower() == "journal":
                self.show_objective()

            elif choice.lower() == "quit":
                print("Thanks for playing!")
                self.game_over = True

            else:
                self.move_player(choice.upper())

                if self.current_location != self.goal:
                    self.generate_encounter()
                    clear_screen()

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

    def show_objective(self):
        print(f"Objective: Go from {self.current_location} to {self.goal}.")

    def suggest_optimal_path(self):
        _, path = dijkstra(self.graph, self.current_location)
        if self.goal in path:
            # Construct the path from the current location to the goal
            next_step = self.goal
            path_to_goal = [next_step]
            while next_step != self.current_location:
                next_step = path[next_step]
                path_to_goal.append(next_step)
            path_to_goal.reverse()
            
            print(f"Suggested optimal path to goal: {' -> '.join(path_to_goal)}")
        else:
            print("You are lost, try exploring some more.")

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
        if self.player.is_alive() and self.current_location == self.goal:
            print(f"You have reached {self.goal}. A menacing presence awaits...")
            boss_battle = BossBattle(self.player)
            boss_battle.battle_soul_of_zinder()
            if self.player.is_alive():
                print("Congratulations! You've defeated the Soul of Zinder and won the game!")
                self.game_over = True
                exit()
            else:
                print("You have fallen in battle... The game is over.")
                self.game_over = True
                exit()
    
    def generate_encounter(self):
        encounter_chance = random.randint(1, 10)

        if encounter_chance <= 7:
            enemy_battle = BattleManager(self.player)
            enemy = Enemy.create_random_enemy()
            enemy_battle.start_battle(enemy)

        else:
            found_items = random.randint(1, 3)

            for _ in range(found_items):
                loot_pool = ["Gold", "Zinder"]
                loot = random.choice(loot_pool)

                if loot == "Gold":
                    gold_amount = random.randint(1, 100)
                    self.player.stats["gold"] += gold_amount
                    input(f"You found {gold_amount} gold!")


                elif loot == "Zinder":
                    self.player.zinders_collected += 1
                    input(f"You found {loot}! You now have {self.player.zinders_collected} Zinders.")

                else:
                    self.player.add_to_inventory(loot)
                    input(f"You found {loot}!")
