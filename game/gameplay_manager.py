import random
from battle_manager import BattleManager
from combat import BossBattle
from character import Enemy
from utils import clear_screen
from dynamic_world_map import dijkstra

"""Manages the gameplay loop, allowing the player to navigate through the world, encounter enemies, and progress towards a goal."""

class GameplayManager:
    def __init__(self, graph, start, goal, player):
        self.graph = graph
        self.current_location = start
        self.start_node = start
        self.goal = goal
        self.player = player
        self.game_over = False
        self.breadcrumbs = [start]
        
    def initiate_gameplay_loop(self):
        while not self.game_over and self.player.is_alive():
            self.display_movement_options()

            # MOVE THIS TO DISPLAY UTILITY CLASS
            print("\nMain Menu:")
            print("--> [Home]         View the Player Menu")
            print("--> [Back]         Go back to the last visited location")
            print("--> [Journal]      See your current objective")
            print("--> [Hint]         View the optimal path to beating the game")
            print("--> [Quit]         Close the game")

            choice = input("\nWhere would you like to go? Enter a path or a menu option: ")
            clear_screen()
            if choice.lower() == "home":
                self.player.navigate_player_menu()
            elif choice.lower() == "hint":
                self.suggest_optimal_path()
            elif choice.lower() == "journal":
                self.show_objective()
            elif choice.lower() == "back":
                if len(self.breadcrumbs) > 1:
                    self.move_player(self.breadcrumbs[-2])
                else:
                    print("You're at the starting location; there's nowhere to go back to.")
            elif choice.lower() == "quit":
                print("Thanks for playing!")
                self.game_over = True
            else:
                if self.move_player(choice.upper()):
                    if self.current_location != self.goal:
                        self.generate_encounter()
                        clear_screen()

                self.check_win_condition()

    def display_movement_options(self):
        possible_moves = self.graph.edges.get(self.current_location, [])
        
        print(f"\nYou are currently at {self.current_location}.\n")
        
        if possible_moves:
            print("You can progress to these location(s):")
            for destination, interaction_type in possible_moves:
                difficulty = self.graph.difficulties[(self.current_location, destination)]
                risk_level = self.difficulty_to_risk_level(difficulty)
                print(f"  {destination} ({interaction_type}): {risk_level}")
        else:
            if len(self.breadcrumbs) > 1:
                last_node = self.breadcrumbs[-2]
                print(f"You have reached a dead end. You can go back to {last_node}.")
            else:
                print("This is the starting node. There are no previous nodes to go back to.")


    def show_objective(self):
        print(f"Objective: Go from {self.current_location} to {self.goal}.")

    def suggest_optimal_path(self):
        _, path = dijkstra(self.graph, self.current_location)
        if self.goal in path:
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
            return True
        elif new_location == self.breadcrumbs[-2] if len(self.breadcrumbs) > 1 else None:
            self.breadcrumbs.pop()
            self.current_location = new_location
            print(f"\nYou have moved back to {new_location}.\n")
            return True
        else:
            print("\nInvalid move. Please try again.\n")
            return False


    def check_win_condition(self):
        if self.player.is_alive() and self.current_location == self.goal:
            print(f"You have reached {self.goal}. A menacing presence awaits...")
            boss_battle = BossBattle(self.player)
            battle_outcome = boss_battle.battle_soul_of_zinder()

            if battle_outcome is True:
                # Victory: The player has defeated the boss.
                print("Congratulations! You've defeated the Soul of Zinder and won the game!")
                self.game_over = True
                exit()
            elif battle_outcome is False:
                # Defeat: The player was defeated by the boss.
                print("You have fallen in battle... The game is over.")
                self.game_over = True
                exit()
            elif battle_outcome is None:
                # Fleeing: The player chose to flee the battle.
                print("You fled from the final battle... The journey is not yet complete.")
                # Reset the player's current location to the start node and clear breadcrumbs.
                self.current_location = self.start_node
                self.breadcrumbs = [self.start_node]
                # The game continues, allowing the player to attempt the battle again.
    
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

