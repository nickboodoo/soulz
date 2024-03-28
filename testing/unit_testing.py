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
        print_dashes(72)
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

    def player_victory(self, enemy):
        print(f"You defeated the {enemy.name}!")
        self.player.enemies_killed += 1

        required_kills = math.ceil(math.log(self.player.level + 1, 2) * 3)
        if self.player.enemies_killed >= required_kills:
            self.player.level_up()
            self.player.enemies_killed = 0

        loot = self.generate_loot()
        self.handle_loot(loot)

    def player_defeat(self):
        input("You lose!")
        exit()

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

class GameplayManager:
    def __init__(self, graph, start, goal, player):
        self.graph = graph
        self.current_location = start
        self.start_node = start  # Add this line to explicitly store the start node
        self.goal = goal
        self.player = player
        self.game_over = False
        self.breadcrumbs = [start]
        

    def display_movement_options(self):
        # Get the current possible moves from the current location
        possible_moves = self.graph.edges.get(self.current_location, [])
        
        print(f"\nYou are currently at {self.current_location}.\n")
        
        # Check if there are forward moves available
        if possible_moves:
            print("You can progress to these location(s):")
            for destination, interaction_type in possible_moves:
                difficulty = self.graph.difficulties[(self.current_location, destination)]
                risk_level = self.difficulty_to_risk_level(difficulty)
                print(f"  {destination} ({interaction_type}): {risk_level}")
        else:
            # If no forward moves, provide an option to move back to the last node, if available
            if len(self.breadcrumbs) > 1:
                last_node = self.breadcrumbs[-2]  # The last node the player was in
                print(f"You have reached a dead end. You can go back to {last_node}.")
            else:
                print("This is the starting node. There are no previous nodes to go back to.")


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
            enemy = Enemy.create_random_enemy()
            battle_manager = BattleManager(self.player)  # Create a BattleManager instance
            battle_screen = BattleScreen(battle_manager, enemy)  # Pass it to BattleScreen
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
    
class Player(Character):
    MAX_HEALTH = 100
    MIN_HEALTH = 0

    def __init__(self, name, god_mode=False):  # Added god_mode parameter
        super().__init__(name, self.MAX_HEALTH, 10)
        self.stats = {"gold": 100}
        self.inventory = {}
        self.enemies_killed = 0
        self.zinders_collected = 0
        self.base_damage = 10
        self.level = 1
        self.god_mode = god_mode  # Added god_mode attribute

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
        if not self.god_mode:  # Only subtract health if god mode is not enabled
            super().defend(damage)  # Call the parent class's defend method

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

    def check_inventory(self):
        print("\nInventory:")

        for item, quantity in self.inventory.items():
            print(f"{item.capitalize()}: {quantity}")


    def use_health_potion(self, item_name, quantity=1):
        if self.health == self.MAX_HEALTH:
            input("Your health is already full.")
            return True  # Indicates that the item use was processed, even if it wasn't effective
        
        heal_amount_per_potion = 20
        total_heal_amount = heal_amount_per_potion * quantity
        self.health += total_heal_amount
        self.health = min(self.MAX_HEALTH, self.health)
        
        self.inventory[item_name] -= quantity
        input(f"You used {quantity} health potion(s) and gained {total_heal_amount} health.")
        return True

    def use_item(self, item):
        # Check if the item is in the inventory or has no stock left
        if item not in self.inventory or self.inventory[item] <= 0:
            input("You don't have that item or you've run out.")
            clear_screen()
            return
        
        # Ask for quantity
        try:
            quantity = int(input(f"How many {item}s do you want to use? "))
        except ValueError:
            input("Invalid number. Please try again.")
            return
        
        # Check if the player has enough of the item
        if self.inventory[item] < quantity:
            input(f"You don't have enough {item}s.")
            clear_screen()
            return
        
        # Handle specific item usage
        if item == "health potion":
            self.use_health_potion(item, quantity)
            clear_screen()

    def print_attack_info(self, lifesteal_percentage, base_damage):
        print(f"Current lifesteal: {lifesteal_percentage*100:.0f}% \nBase damage range: {base_damage} - {base_damage + 10}.")

    def view_character_stats(self):
        lifesteal_percentage = self.zinders_collected * 0.01
        print("\nCharacter Stats:")
        print(f"Health: {self.health}/{self.MAX_HEALTH}")
        print(f"Level: {self.level}")
        print(f"Current lifesteal: {lifesteal_percentage*100:.0f}%")
        print(f"Attack damage range: {self.base_damage} - {self.base_damage + 10}")
    

    def print_status(self, enemy=None):
        print(f"{self.name} - HP: {'█' * int(self.health / 5)} ({self.health}/{self.MAX_HEALTH})\n".rjust(72))
        if enemy:
            print(f"{enemy.name} - HP: {'█' * int(enemy.health / 5)} ({enemy.health}/100)\n".rjust(72))


    def print_player_menu(self):
        print("\nPLAYER MENU")
        print("What would you like to do?")
        print("[b]uy items")
        print("[c]heck inventory")
        print("[u]se item from inventory")
        print("[s]how character stats")
        print("[t]ravel to tavern")
        print("[l]eave city")

    def stay_at_tavern(self):
        print("You decide to stay at the tavern for a rest.")
        self.health = self.MAX_HEALTH
        input("Your health has been fully restored.")
        clear_screen()

    def buy_items(self):
        store_items = {
            "health potion": 20,  # Cost per item
        }
        print("\nWelcome to the store!")
        print("Here are the items available for purchase:")

        while True:
            print("\nYour Gold:", self.stats["gold"])
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
                        raise ValueError  # Handle non-positive integers
                except ValueError:
                    print("Please enter a valid number.")
                    input("Press Enter to continue...")
                    clear_screen()
                    continue

                total_cost = store_items[item_choice] * quantity
                if self.stats["gold"] >= total_cost:
                    self.add_to_inventory(item_choice, quantity)
                    self.stats["gold"] -= total_cost
                    print(f"You bought {quantity} {item_choice}(s) for {total_cost} gold!")
                    input("Press Enter to continue...")
                    clear_screen()
                else:
                    print("You don't have enough gold for that purchase.")
                    input("Press Enter to continue...")
                    clear_screen()
            else:
                print("That item is not available in the store.")
                input("Press Enter to continue...")
                clear_screen()

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
    
class BossBattle(Combat):
    def __init__(self, player):
        super().__init__(player)
        self.soul_of_zinder = Enemy("Soul of Zinder", 100, 55)  # Assuming Enemy class definition

    def battle_soul_of_zinder(self):
        clear_screen()
        print(f"The {self.soul_of_zinder.name} appears!")
        input("Prepare yourself for a challenging battle!")

        while self.check_alive(self.player) and self.check_alive(self.soul_of_zinder):
            self.player.print_status(self.soul_of_zinder)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()
            clear_screen()

            if choice == "a":
                self.initiate_attack(self.player, self.soul_of_zinder)
                if self.check_alive(self.soul_of_zinder):
                    self.initiate_attack(self.soul_of_zinder, self.player)

            elif choice == "u":
                self.player.check_inventory()
                item_to_use = input("Enter the item you want to use (or [cancel] to go back): ").lower()
                clear_screen()

                if item_to_use == "cancel":
                    continue
                self.player.use_item(item_to_use)

            elif choice == "f":
                print("You fled from the battle!")
                return
            
            else:
                print("Invalid choice. Please try again.")

        if self.player.is_alive():
            print(f"Congratulations! You defeated the {self.soul_of_zinder.name}!")
            input("Thank for playing. Click ENTER to exit.")
            return True

        elif not self.player.is_alive():
            print("You lost the battle against the Soul of Zinder!")
            return False

        else:
            # Player fled
            return None

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

class ScreenManager:
    def __init__(self, player):
        self.player = player
        self.screens = {
            'b': BuyItemsScreen(player),
            'c': InventoryScreen(player),
            'u': UseItemScreen(player),  # Update this line to use UseItemScreen
            's': CharacterStatsScreen(player),
            't': StayAtTavernScreen(player),
        }

    def add_screen(self, key, screen):
        self.screens[key] = screen

    def navigate_to(self, key):
        if key in self.screens:
            self.screens[key].display()
            self.screens[key].handle_input()
    
    def navigate(self):
        while True:
            print("\nAvailable Screens:")
            for key in self.screens:
                print(f"- {key}")

            choice = input("Enter the screen you want to navigate to, or type 'exit' to return: ").lower()

            if choice == 'exit':
                break
            elif choice in self.screens:
                self.navigate_to(choice)
            else:
                print("Invalid choice. Please try again.")

    def navigate_player(self):
        self.exit_screen_navigation = False  # Reset the flag each time navigation starts
        while True:
            self.print_player_menu()
            choice = input("Enter your choice: ").lower()
            clear_screen()

            if choice in self.screens:
                self.screens[choice].display()
                self.screens[choice].handle_input()
            elif choice == "l":
                self.exit_screen_navigation = True  # Set the flag when leaving
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
                # Implement using item logic here or in the battle manager
                pass
            elif choice == "f":
                print("You fled from the battle!")
                break
            else:
                print("Invalid choice. Please try again.")

            if not self.enemy.is_alive():
                print(f"You defeated the {self.enemy.name}!")
                self.battle_manager.handle_battle_outcome(self.enemy)
                break

        if not self.battle_manager.player.is_alive():
            print("You lose!")

class UseItemScreen(Screen):
    def display(self):
        # First, display the inventory to the player.
        self.player.check_inventory()
        print("Enter the name of the item you want to use, or type [cancel] to go back.")

    def handle_input(self):
        item_to_use = input("Choose an item to use: ").lower()
        
        # If the player decides not to use an item
        if item_to_use == "cancel":
            print("You chose not to use any item.")
            return

        # Check if the item is in the inventory or has no stock left
        if item_to_use not in self.player.inventory or self.player.inventory[item_to_use] <= 0:
            print("You don't have that item or you've run out.")
            return

        # Ask for quantity (this part can be adjusted based on how you want to handle quantities)
        try:
            quantity = int(input(f"How many {item_to_use}s do you want to use? "))
        except ValueError:
            print("Invalid number. Please try again.")
            return

        # Use the item
        if self.player.use_item(item_to_use, quantity):
            print(f"Used {quantity} of {item_to_use}.")
        else:
            print(f"Could not use {item_to_use}.")

class NavigationMenuScreen:
    def __init__(self, game_manager):
        self.game_manager = game_manager

    def display(self):
        while not self.game_manager.game_over and self.game_manager.player.is_alive():
            self.game_manager.display_movement_options()
            print("\nMain Menu:")
            print("--> [Home]         View the Player Menu")
            print("--> [Back]         Go back to the last visited location")
            print("--> [Journal]      See your current objective")
            print("--> [Hint]         View the optimal path to beating the game")
            print("--> [Quit]         Close the game")
            choice = input("\nWhere would you like to go? Enter a path or a menu option: ")
            clear_screen()

            if choice.lower() == "home":
                # Instead of calling navigate(), directly call navigate_player()
                # which uses print_player_menu for displaying options
                exit_navigation = self.game_manager.screen_manager.navigate_player()
                if exit_navigation:  # Check if the navigation requested an exit to possibly end the game or return to a higher level menu
                    return

            elif choice.lower() == "hint":
                self.game_manager.suggest_optimal_path()
            
            elif choice.lower() == "journal":
                self.game_manager.show_objective()

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
        input("Press Enter to continue...")  # Assuming clear_screen() is called elsewhere

class CharacterStatsScreen(Screen):
    def display(self):
        self.player.view_character_stats()

    def handle_input(self):
        input("Press Enter to continue...")

class BuyItemsScreen(Screen):
    def display(self):
        self.player.buy_items()

    def handle_input(self):
        pass  # Buy items logic is handled within the display method

class StayAtTavernScreen(Screen):
    def display(self):
        self.player.stay_at_tavern()

    def handle_input(self):
        input("Press Enter to continue...")

class GameEngine:
    def __init__(self):
        self.setup = GameSetup()

    def run(self):
        self.setup.initialize_game_settings("A", "D")
        self.setup.setup_map()
        intro_screen = IntroScreen(self.setup)
        intro_screen.display_intro()
        self.setup.setup_game()
        
        # Initialize ScreenManager and assign it to GamePlayManager for access from NavigationMenuScreen
        self.setup.game_manager.screen_manager = ScreenManager(self.setup.player)

        while not self.setup.game_manager.game_over:
            navigation_menu = NavigationMenuScreen(self.setup.game_manager)
            navigation_menu.display()

        print("Game Over. Thanks for playing!")

if __name__ == "__main__":
    game_engine = GameEngine()
    game_engine.run()
