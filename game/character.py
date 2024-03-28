import random
from utils import clear_screen

"""A base class for all characters in the game (both the player and enemies), 
containing common attributes like health, attack power, and basic actions like attack and defend."""

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
    

"""Inherits from the Character class, adding specific attributes and functionalities for the player,
including inventory management, character stats like level and lifesteal, and the ability to use items."""

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

    def navigate_player_menu(self):
        while True:
            self.print_player_menu()
            choice = input("Enter your choice: ").lower()
            clear_screen()
            if choice == "b":
                self.buy_items()
            elif choice == "c":
                self.check_inventory()
            elif choice == "u":
                self.check_inventory()
                item_to_use = input("Enter the item you want to use from your inventory: ").lower()
                clear_screen()
                self.use_item(item_to_use)
            elif choice == "s":
                self.view_character_stats()
            elif choice == "t":
                self.stay_at_tavern()
            elif choice == "l":
                input("You leave the city.")
                clear_screen()
                break
            else:
                print("Invalid choice. Please try again.")

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



"""Also inherits from the Character class, representing various enemies in the game.
It includes a class method to create random enemy types."""

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
    