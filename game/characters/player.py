import random
from characters.character import Character
from utility.utils import clear_screen

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
        if not self.god_mode:  # Check if god_mode is active
            self.health = max(self.MIN_HEALTH, self.health - damage)

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
