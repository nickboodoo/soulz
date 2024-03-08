import random

from game.character import Character


class Player(Character):
    MAX_HEALTH = 100
    MIN_HEALTH = 0

    def __init__(self, name):
        super().__init__(name, self.MAX_HEALTH, 10)  # Initialize the parent class
        self.stats = {"gold": 100}  # Player stats
        self.inventory = {}  # Player inventory
        self.enemies_killed = 0  # Number of enemies the player has killed
        self.zinders_collected = 0  # Number of Zinders collected
        self.base_damage = 10  # Define base_damage here if used in attack calculations
        self.level = 1  # Initialize the player's level

    # The rest of the Player class remains the same

    def level_up(self):
        self.level += 1  # Increment the player's level
        self.base_damage += 5  # Increase base damage or other stats as appropriate
        print(f"Congratulations! You've reached level {self.level}. Your base damage has increased.")
        # Additional level up logic can go here (e.g., increasing max health, restoring health, etc.)


    def attack(self):
        lifesteal_percentage = self.zinders_collected * 0.01
        # Now base_damage is properly defined, this should work:
        lifesteal_amount = int(self.base_damage * lifesteal_percentage)
        self.health += lifesteal_amount  # Assuming you want to add the lifesteal amount to the player's health
        self.health = min(self.MAX_HEALTH, self.health)  # Ensure health doesn't exceed MAX_HEALTH
        return random.randint(self.base_damage, self.base_damage + 10)  # Use base_damage for attack calculation

    # The rest of the Player class remains unchanged


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

    def use_item(self, item):
        if item in self.inventory and self.inventory[item] > 0:
            if item == "health potion":
                if self.health == self.MAX_HEALTH:
                    print("Your health is already full.")
                else:
                    heal_amount = 20  # Define how much health is restored by a potion
                    self.health = min(self.MAX_HEALTH, self.health + heal_amount)
                    self.inventory[item] -= 1  # Use up one health potion
                    print(f"You used a health potion and gained {heal_amount} health.")
            else:
                print("You cannot use that item.")
        else:
            print("You don't have that item or you've run out.")

    def view_character_stats(self):
        print("\nCharacter Stats:")
        print(f"Health: {self.health}/{self.MAX_HEALTH}")

    def level_up(self):
        self.level += 1
        self.base_damage += 5
        print(f"Congratulations! You've reached level {self.level}. Your base damage has increased.")