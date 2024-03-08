import random

class Player:
    MAX_HEALTH = 100
    MIN_HEALTH = 0

    def __init__(self, name):
        self.name = name
        self.stats = {"health": self.MAX_HEALTH, "gold": 100}
        self.level = 1
        self.base_damage = 10
        self.inventory = {}
        self.enemies_killed = 0
        self.zinders_collected = 0 

    def attack(self):
        lifesteal_percentage = self.zinders_collected * 0.01
        lifesteal_amount = int(self.base_damage * lifesteal_percentage)
        self.stats["health"] = min(self.MAX_HEALTH, self.stats["health"] + lifesteal_amount)
        return random.randint(self.base_damage, self.base_damage + 10)  # Increase damage range

    def defend(self, damage):
        self.stats["health"] -= damage
        self.stats["health"] = max(self.MIN_HEALTH, self.stats["health"])

    def is_alive(self):
        return self.stats["health"] > self.MIN_HEALTH

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
        if item in self.inventory:

            if item == "health potion":

                if self.stats["health"] == self.MAX_HEALTH:

                    print("Your health is already full.")

                else:
                    self.stats["health"] = min(self.MAX_HEALTH, self.stats["health"] + 20)
                    self.remove_from_inventory(item)
                    print(f"You used a health potion and gained 20 health.")

            else:
                print("You cannot use that item.")

        else:
            print("You don't have that item.")

    def view_character_stats(self):
        print("\nCharacter Stats:")
        print(f"Health: {self.stats['health']}/{self.MAX_HEALTH}")
        print(f"Level: {self.level}")

    def level_up(self):
        self.level += 1
        self.base_damage += 5
        print(f"Congratulations! You've reached level {self.level}. Your base damage has increased.")

        