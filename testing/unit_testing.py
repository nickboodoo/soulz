import math
import random
import os

class Combat:
    def __init__(self, player):
        self.player = player

    def initiate_attack(self, attacker, defender):
        damage = attacker.attack()
        defender.defend(damage)
        print(f"{attacker.name} attacks {defender.name} for {damage} damage.".center(72))

    def check_alive(self, character):
        return character.is_alive()

class BattleManager(Combat):
    def __init__(self, player):
        super().__init__(player)

    def player_attack(self, enemy):
        player_damage = self.player.attack()
        enemy.defend(player_damage)
        print(f"{self.player.name} attacks the {enemy.name} for {player_damage} damage.".center(72))

    def enemy_attack(self, enemy):
        enemy_damage = enemy.attack()
        self.player.defend(enemy_damage)
        print(f"The {enemy.name} attacks back for {enemy_damage} damage.".center(72))

    def handle_battle_outcome(self, enemy):
        if self.player.is_alive():
            self.player_victory(enemy)
        else:
            self.player_defeat()
# 3 SCREENS
class GameplayManager:
    def __init__(self, graph, start, goal, player):
        self.graph = graph
        self.current_location = start
        self.start_node = start
        self.goal = goal
        self.player = player
        self.game_over = False
        self.breadcrumbs = [start]
        self.final_enemy = Enemy("Gwyn, Lord of Sunlight", 150, 50)

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
            # Initiating final battle with battle screen instead of directly in GameplayManager
            self.initiate_final_battle()
        
    def initiate_final_battle(self):
        # Create a BattleManager instance for the final battle
        final_battle_manager = BattleManager(self.player)
        
        # Then pass this BattleManager instance along with the final enemy to the BattleScreen
        final_battle_screen = BattleScreen(final_battle_manager, self.final_enemy)
        final_battle_screen.display()
        
        # Use the modified or existing handle_input method for final battle interaction
        # This might require adjusting handle_input to accommodate final battle logic
        final_battle_screen.handle_input()

        # Check outcomes after the battle screen interaction finishes
        if not self.player.is_alive():
            print("You have fallen in the final battle... The game is over.")
            self.game_over = True
        elif not self.final_enemy.is_alive():
            print("Congratulations! You've defeated the Guardian of the Goal and won the game!")
            self.game_over = True
        else:
            # Handle fleeing scenario
            self.current_location = self.start_node
            print("Fled back to the start. The journey continues...")
    
    def generate_encounter(self):
        encounter_chance = random.randint(1, 10)

        if encounter_chance <= 7:
            enemy = Enemy.create_random_enemy()
            battle_manager = BattleManager(self.player)
            battle_screen = BattleScreen(battle_manager, enemy)
            self.screen_manager.add_screen('battle', battle_screen)
            self.screen_manager.navigate_to('battle')
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

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self):
        return random.randint(5, self.attack_power)

    def defend(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0
# 2 SCREENS    
class Player(Character):
    MAX_HEALTH = 100
    MIN_HEALTH = 0

    def __init__(self, name, god_mode=False):
        super().__init__(name, self.MAX_HEALTH, 10)
        self.stats = {"gold": 100}
        self.inventory = {}
        self.enemies_killed = 0
        self.zinders_collected = 0
        self.base_damage = 10
        self.level = 1
        self.god_mode = god_mode

    # MOVE THIS INTO ITS OWN SCREEN CLASS
    def level_up(self):
        self.level += 1
        self.base_damage += 5
        input(f"Congratulations! You've reached level {self.level}. Your base damage has increased.")

    def attack(self):
        lifesteal_percentage = self.zinders_collected * 0.01
        lifesteal_amount = int(self.base_damage * lifesteal_percentage)
        self.health += lifesteal_amount
        self.health = min(self.MAX_HEALTH, self.health)
        return random.randint(self.base_damage, self.base_damage + 10)

    def defend(self, damage):
        if not self.god_mode:
            super().defend(damage)

    def is_alive(self):
        return self.health > self.MIN_HEALTH

    def add_to_inventory(self, item, quantity=1):
        if item in self.inventory:
            self.inventory[item] += quantity

        else:
            self.inventory[item] = quantity

    def remove_from_inventory(self, item, quantity=1):
        if item in self.inventory:

            if self.inventory[item] >= quantity:
                self.inventory[item] -= quantity
                return True
            
        return False

    # MOVE THIS INTO ITS OWN SCREEN CLASS
    def check_inventory(self):
        print("\nInventory:")

        for item, quantity in self.inventory.items():
            print(f"{item.capitalize()}: {quantity}")

    def print_attack_info(self, lifesteal_percentage, base_damage):
        print(f"Current lifesteal: {lifesteal_percentage*100:.0f}% \nBase damage range: {base_damage} - {base_damage + 10}.")
    
    def print_status(self, enemy=None):
        print(f"{self.name} - HP: {'█' * int(self.health / 5)} ({self.health}/{self.MAX_HEALTH})\n".rjust(72))
        if enemy:
            print(f"{enemy.name} - HP: {'█' * int(enemy.health / 5)} ({enemy.health}/100)\n".rjust(72))

class Enemy(Character):
    def __init__(self, name, health, attack_power):
        super().__init__(name, health, attack_power)

    @classmethod
    def create_random_enemy(cls):
        enemy_types = [
            ("Abyssal Revenant", 50, 25),
            ("Crimson Shade", 60, 22),
            ("Dreadbone Wraith", 35, 30),
            ("Spectral Sentinel", 80, 15),
            ("Netherghast Fiend", 40, 20),
            ("Voidborne Behemoth", 100, 17),
            ("Rimefrost Phantom", 65, 18),
            ("Shadowveil Assassin", 45, 25),
            ("Infernal Chimera", 90, 22),
            ("Searing Phoenix", 70, 22),
            ("Eldritch Gorgon", 85, 35),
        ]
        
        name, health, attack_power = random.choice(enemy_types)
        return cls(name, health, attack_power)
    
class Combat:
    def __init__(self, player):
        self.player = player

    def initiate_attack(self, attacker, defender):
        damage = attacker.attack()
        defender.defend(damage)
        print(f"{attacker.name} attacks {defender.name} for {damage} damage.".center(72))

    def check_alive(self, character):
        return character.is_alive()
# 1 SCREEN
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

class GameSetup:
    def __init__(self):
        self.node_difficulties = []
        self.start_node = None
        self.end_node = None
        self.graph = None
        self.game = None
        self.player = None

    def initialize_game_settings(self, start_node, end_node):
        self.node_difficulties = [("A", 0.7), ("B", 0.4), ("C", 0.9), ("D", 0.5), ("E", 0.8), ("F", 0.6)]

        self.start_node = start_node
        self.end_node = end_node

    def initialize_player(self):
        god_mode_input = input("Welcome to Soulz! ")
        god_mode_enabled = god_mode_input.lower() == "tgm"

        player_name = input("Enter your name: ")
        self.player = Player(player_name, god_mode=god_mode_enabled)

    def setup_map(self):
        self.graph = DynamicWorldMap()
        self.graph.generate_graph(self.node_difficulties)
    
    def setup_game(self):
        self.game_manager = GameplayManager(self.graph, self.start_node, self.end_node, self.player)

    def initiate_gameplay_loop(self):
        if self.game:
            self.game.initiate_gameplay_loop()
        else:
            print("Game not set up. Call setup_game first.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_dashes(x):
    dash = '-'
    border = dash * x
    print(border)

#========================================================================================================#
#                                             SCREEN STUFF                                               #
#========================================================================================================#

class Screen:
    def __init__(self, player):
        self.player = player

    def display(self):
        pass

    def handle_input(self):
        pass

class PlayerMenuScreen:
    def __init__(self, player):
        self.player = player
        self.screens = {
            'b': BuyItemsScreen(player),
            'c': InventoryScreen(player),
            'u': UseItemScreen(player),
            's': CharacterStatsScreen(player),
            't': StayAtTavernScreen(player),
        }

    def add_screen(self, key, screen):
        self.screens[key] = screen

    def navigate_to(self, key):
        if key in self.screens:
            self.screens[key].display()
            self.screens[key].handle_input()

    def navigate_player(self):
        self.exit_screen_navigation = False
        while True:
            self.print_player_menu()
            choice = input("Enter your choice: ").lower()
            clear_screen()

            if choice in self.screens:
                self.screens[choice].display()
                self.screens[choice].handle_input()
            elif choice == "l":
                self.exit_screen_navigation = True
                break
            else:
                print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

        return self.exit_screen_navigation

    def print_player_menu(self):
        print("\nPLAYER MENU")
        print("What would you like to do?")
        print("[b]uy items")
        print("[c]heck inventory")
        print("[u]se item from inventory")
        print("[s]how character stats")
        print("[t]ravel to tavern")
        print("[l]eave city")

class MovementOptionsScreen(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager.player)
        self.game_manager = game_manager

    def display(self):
        possible_moves = self.game_manager.graph.edges.get(self.game_manager.current_location, [])
        
        print(f"\nYou are currently at {self.game_manager.current_location}.\n")
        
        if possible_moves:
            print("You can progress to these location(s):")
            for destination, interaction_type in possible_moves:
                difficulty = self.game_manager.graph.difficulties[(self.game_manager.current_location, destination)]
                risk_level = self.game_manager.difficulty_to_risk_level(difficulty)
                print(f"  {destination} ({interaction_type}): {risk_level}")
        
        if len(self.game_manager.breadcrumbs) > 1:
            last_visited_node = self.game_manager.breadcrumbs[-2]
            print(f"Your last visited node was {last_visited_node}.")

    def handle_input(self):
        choice = input("\nChoose your next location (or type 'Back' to return): ").capitalize()

        if choice == 'Back':
            if len(self.game_manager.breadcrumbs) > 1:
                # Move back to the previous location
                self.game_manager.breadcrumbs.pop()  # Remove current location from breadcrumbs
                back_location = self.game_manager.breadcrumbs[-1]  # Get last location
                self.game_manager.current_location = back_location  # Update current location
                print(f"\nYou have moved back to {back_location}.\n")
            else:
                print("\nYou are at the start location. There's nowhere to go back.\n")
        else:
            self.move_player(choice)

    def move_player(self, new_location):
        if new_location in [edge[0] for edge in self.game_manager.graph.edges.get(self.game_manager.current_location, [])]:
            self.game_manager.breadcrumbs.append(new_location)
            self.game_manager.current_location = new_location
            print(f"\nYou have moved to {new_location}.\n")
        else:
            print("\nInvalid move. Please try again.\n")


class ObjectiveScreen(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager.player)
        self.game_manager = game_manager

    def display(self):
        print(f"Objective: Go from {self.game_manager.current_location} to {self.game_manager.goal}.")

class OptimalPathScreen(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager.player)
        self.game_manager = game_manager

    def display(self):
        _, path = dijkstra(self.game_manager.graph, self.game_manager.current_location)
        if self.game_manager.goal in path:
            next_step = self.game_manager.goal
            path_to_goal = [next_step]
            while next_step != self.game_manager.current_location:
                next_step = path[next_step]
                path_to_goal.append(next_step)
            path_to_goal.reverse()
            
            print(f"Suggested optimal path to goal: {' -> '.join(path_to_goal)}")
        else:
            print("You are lost, try exploring some more.")


class VictoryScreen(Screen):
    def __init__(self, player, enemy):
        super().__init__(player)
        self.enemy = enemy

    def display(self):
        print(f"You defeated the {self.enemy.name}!")
        self.player.enemies_killed += 1

        required_kills = math.ceil(math.log(self.player.level + 1, 2) * 3)
        if self.player.enemies_killed >= required_kills:
            self.player.level_up()
            self.player.enemies_killed = 0

        loot = self.generate_loot()
        self.handle_loot(loot)

    def generate_loot(self):
        loot_pool = ["Gold", "Zinder"]
        return random.choice(loot_pool)

    def handle_loot(self, loot):
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

class BattleScreen(Screen):
    def __init__(self, battle_manager, enemy):
        super().__init__(battle_manager.player)
        self.battle_manager = battle_manager
        self.enemy = enemy

    def display(self):
        clear_screen()
        print_dashes(72)
        print(f"You've encountered a {self.enemy.name}!".center(72))

    def handle_input(self):
        while self.battle_manager.player.is_alive() and self.enemy.is_alive():
            self.battle_manager.player.print_status(self.enemy)
            print_dashes(72)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()
            clear_screen()

            if choice == "a":
                self.battle_manager.initiate_attack(self.battle_manager.player, self.enemy)
                if self.enemy.is_alive():
                    self.battle_manager.initiate_attack(self.enemy, self.battle_manager.player)
            elif choice == "u":
                item_screen = UseItemScreen(self.player)
                item_screen.display()
                item_screen.handle_input()
                if self.enemy.is_alive():
                    self.battle_manager.initiate_attack(self.enemy, self.battle_manager.player)
            elif choice == "f":
                print("You fled from the battle!")
                break
            else:
                print("Invalid choice. Please try again.")

            if not self.enemy.is_alive():
                victory_screen = VictoryScreen(self.battle_manager.player, self.enemy)
                victory_screen.display()
                break

        if not self.battle_manager.player.is_alive():
            print("You lose!")

class UseItemScreen(Screen):
    def __init__(self, player):
        super().__init__(player)

    def display(self):
        self.player.check_inventory()
        print("Enter the name of the item you want to use, or type [cancel] to go back.")

    def handle_input(self):
        item_name = input("Choose an item to use: ").lower()
        
        if item_name == "cancel":
            print("You chose not to use any item.")
            return

        if item_name not in self.player.inventory or self.player.inventory[item_name] <= 0:
            print("You don't have that item or you've run out.")
            return

        try:
            quantity = int(input(f"How many {item_name}s do you want to use? "))
            if quantity <= 0:
                raise ValueError("Invalid quantity.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            return

        self.use_item(item_name, quantity)

    def use_item(self, item_name, quantity):
        if item_name == "health potion":
            if self.player.health == self.player.MAX_HEALTH:
                print("Your health is already full.")
                return
            heal_amount_per_potion = 20
            total_heal_amount = heal_amount_per_potion * quantity
            self.player.health += total_heal_amount
            self.player.health = min(self.player.health, self.player.MAX_HEALTH)
            self.player.inventory[item_name] -= quantity
            if self.player.inventory[item_name] <= 0:
                del self.player.inventory[item_name]
            print(f"You used {quantity} {item_name}(s) and gained {total_heal_amount} health.")
        else:
            print(f"The {item_name} cannot be used this way.")

class NavigationMenuScreen:
    def __init__(self, game_manager):
        self.game_manager = game_manager

    def display(self):
        while not self.game_manager.game_over and self.game_manager.player.is_alive():
            # Commented out because display_movement_options no longer exists in GameplayManager
            # self.game_manager.display_movement_options()
            print("\nMain Menu:")
            print("--> [Move]         Show movement options and move")
            print("--> [Home]         View the Player Menu")
            print("--> [Back]         Go back to the last visited location")
            print("--> [Journal]      See your current objective")
            print("--> [Hint]         View the optimal path to beating the game")
            print("--> [Quit]         Close the game")
            choice = input("\nWhere would you like to go? Enter a path or a menu option: ").lower()
            clear_screen()

            if choice == "move":
                # Here we instantiate and display MovementOptionsScreen
                movement_options_screen = MovementOptionsScreen(self.game_manager)
                movement_options_screen.display()

            elif choice.lower() == "home":
                exit_navigation = self.game_manager.screen_manager.navigate_player()
                if exit_navigation:
                    return

            elif choice.lower() == "hint":
                optimal_path_screen = OptimalPathScreen(self.game_manager)
                optimal_path_screen.display()
            
            elif choice.lower() == "journal":
                objective_screen = ObjectiveScreen(self.game_manager)
                objective_screen.display()

            elif choice.lower() == "back":
                if len(self.game_manager.breadcrumbs) > 1:
                    self.game_manager.move_player(self.game_manager.breadcrumbs[-2])
                else:
                    print("You're at the starting location; there's nowhere to go back to.")

            elif choice.lower() == "quit":
                print("Thanks for playing!")
                self.game_manager.game_over = True

            else:
                if self.game_manager.move_player(choice.upper()):
                    if self.game_manager.current_location != self.game_manager.goal:
                        self.game_manager.generate_encounter()
                        clear_screen()

                self.game_manager.check_win_condition()

class IntroScreen:
    def __init__(self, setup):
        self.setup = setup

    def display_intro(self):
        self.setup.initialize_player()
        clear_screen()

class InventoryScreen(Screen):
    def display(self):
        self.player.check_inventory()

    def handle_input(self):
        item_to_use = input("Enter the item you want to use from your inventory: ").lower()
        self.player.use_item(item_to_use)
        input("Press Enter to continue...")

class CharacterStatsScreen(Screen):
    def display(self):
        lifesteal_percentage = self.player.zinders_collected * 0.01
        print("\nCharacter Stats:")
        print(f"Health: {self.player.health}/{self.player.MAX_HEALTH}")
        print(f"Level: {self.player.level}")
        print(f"Base Damage: {self.player.base_damage}")
        print(f"Zinders Collected: {self.player.zinders_collected}")
        print(f"Current Lifesteal: {lifesteal_percentage*100:.0f}%")
        print(f"Attack Damage Range: {self.player.base_damage} - {self.player.base_damage + 10}")
        print(f"Gold: {self.player.stats['gold']}")
        self.handle_input()

    def handle_input(self):
        input("\nPress Enter to go back...")
        clear_screen()

class BuyItemsScreen(Screen):
    def display(self):
        print("\nWelcome to the store!")
        print("Here are the items available for purchase:")
        store_items = {
            "health potion": 20,
        }
        while True:
            print("\nYour Gold:", self.player.stats["gold"])
            for item, price in store_items.items():
                print(f"{item.capitalize()} - {price} gold each")

            item_choice = input("\nEnter the item you want to buy (or [done] to exit): ").lower()
            clear_screen()

            if item_choice == "done":
                break

            elif item_choice in store_items:
                try:
                    quantity = int(input(f"How many {item_choice}s would you like to buy? "))
                    if quantity <= 0:
                        raise ValueError
                except ValueError:
                    print("Please enter a valid number.")
                    continue

                total_cost = store_items[item_choice] * quantity
                if self.player.stats["gold"] >= total_cost:
                    self.player.add_to_inventory(item_choice, quantity)
                    self.player.stats["gold"] -= total_cost
                    print(f"You bought {quantity} {item_choice}(s) for {total_cost} gold!")
                else:
                    print("You don't have enough gold for that purchase.")
            else:
                print("That item is not available in the store.")

class StayAtTavernScreen(Screen):
    def display(self):
        print("You decide to stay at the tavern for a rest.")

        self.player.health = self.player.MAX_HEALTH

        input("Your health has been fully restored.")
        clear_screen()
# 1 Screen
class GameEngine:
    def __init__(self):
        self.setup = GameSetup()

    def run(self):
        self.setup.initialize_game_settings("A", "D")
        self.setup.setup_map()
        intro_screen = IntroScreen(self.setup)
        intro_screen.display_intro()
        self.setup.setup_game()
        
        self.setup.game_manager.screen_manager = PlayerMenuScreen(self.setup.player)

        while not self.setup.game_manager.game_over:
            navigation_menu = NavigationMenuScreen(self.setup.game_manager)
            navigation_menu.display()

        # MOVE THIS INTO ITS OWN SCREEN CLASS
        print("Game Over. Thanks for playing!")

if __name__ == "__main__":
    game_engine = GameEngine()
    game_engine.run()
