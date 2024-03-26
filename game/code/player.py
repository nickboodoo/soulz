import random
from code.character import Character
from code.utils import clear_screen

"""Inherits from the Character class, adding specific attributes and functionalities for the player,
including inventory management, character stats like level and lifesteal, and the ability to use items."""

class Player(Character):
    MAX_HEALTH = 100
    MIN_HEALTH = 0

    def __init__(self, name):
        super().__init__(name, self.MAX_HEALTH, 10)
        self.stats = {"gold": 100}
        self.inventory = {}
        self.enemies_killed = 0
        self.zinders_collected = 0
        self.base_damage = 10
        self.level = 1

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


    def use_health_potion(self, item_name):
        if self.health == self.MAX_HEALTH:
            input("Your health is already full.")
            return True  # Indicates that the item use was processed, even if it wasn't effective
        heal_amount = 20
        self.health = min(self.MAX_HEALTH, self.health + heal_amount)
        self.inventory[item_name] -= 1
        input(f"You used a health potion and gained {heal_amount} health.")
        return True


    def use_item(self, item):
        # Check if the item is not in the inventory or has no stock left
        if item not in self.inventory or self.inventory[item] <= 0:
            input("You don't have that item or you've run out.")
            clear_screen()
            return
        
        # Handle specific item usage
        if item == "health potion":
            if self.use_health_potion(item):
                clear_screen()
                return

        # If the item doesn't match any known item
        input("You cannot use that item.")
        clear_screen()

    def print_attack_info(lifesteal_percentage, base_damage):
        print(f"Current lifesteal: {lifesteal_percentage*100:.0f}% \nBase damage range: {base_damage} - {base_damage + 10}.")

    def view_character_stats(self):
        lifesteal_percentage = self.zinders_collected * 0.01
        print("\nCharacter Stats:")
        print(f"Health: {self.health}/{self.MAX_HEALTH}")
        print(f"Level: {self.level}")
        print(f"Current lifesteal: {lifesteal_percentage*100:.0f}%")
        print(f"Attack damage range: {self.base_damage} - {self.base_damage + 10}")

    def level_up(self):
        self.level += 1
        self.base_damage += 5
        input(f"Congratulations! You've reached level {self.level}. Your base damage has increased.")