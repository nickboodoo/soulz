import random
from battle_manager import BattleManager
from boss_battle import BossBattle
from enemy import Enemy
from utils import clear_screen, navigate_player_menu
from utils import dijkstra


class GameplayManager:
    def __init__(self, graph, start, goal, player):
        self.graph = graph
        self.current_location = start
        self.goal = goal
        self.player = player
        self.game_over = False
        self.breadcrumbs = [start]
        

    def initiate_gameplay_loop(self):
        print(f"Objective: Go from {self.current_location} to {self.goal}.")

        while self.player.is_alive():
            self.display_movement_options()
            choice = input("Where would you like to go? ")
            if choice.lower() == "menu":
                # REFACTOR THIS 
                navigate_player_menu(self.player)

            elif choice.lower() == "quit":
                print("Thanks for playing!")
                break

            else:
                self.move_player(choice.upper())
                self.generate_encounter()
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
        if self.player.is_alive() and self.current_location == self.goal:
            print(f"Congratulations! You've reached {self.goal} and won the game!")
            self.game_over = True
            exit()
        if not self.player.is_alive():
            print("Game over.")
    
    # RUN THIS LOOP WHEN THE PLAYER STARTS THE GAME OR FINISHES ENCOUNTER AT A NODE (i think)
    

    # OVERHAUL THIS CONCEPT
    def generate_encounter(self):
        encounter_chance = random.randint(1, 10)

        if encounter_chance <= 7:
            enemy_battle = BattleManager(self.player)
            enemy = Enemy.create_random_enemy()
            enemy_battle.start_battle(enemy)

        else:
            found_items = random.randint(1, 3)

            for _ in range(found_items):
                loot_pool = ["Ancient Runestone", "Gold", "Zinder"]
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

            if "Ancient Runestone" in self.player.inventory and self.player.inventory["Ancient Runestone"] >= 4:
                final_boss_battle = BossBattle(self.player)
                final_boss_battle.battle_soul_of_zinder()