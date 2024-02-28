import random

class Player:
    MAX_HEALTH = 100
    MIN_HEALTH = 0

    def __init__(self, name):
        self.name = name
        self.stats = {"health": self.MAX_HEALTH, "mana": 50, "gold": 100}
        self.equipped_items = {"weapon": None, "armor": None}
        self.inventory = {"health potion": 2, "mana potion": 1}
        self.enemies_killed = 0
        self.distance_travelled = 0
        self.encounters = []
        self.quest_items_collected = set()  # Initialize quest items collected as an empty set

    def attack(self):
        attack_bonus = self.equipped_items["weapon"].get("attack_bonus", 0) if self.equipped_items["weapon"] else 0
        return random.randint(10, 20) + attack_bonus

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
        print(f"Mana: {self.stats['mana']}/100")
        print("Equipped Items:")
        for slot, item in self.equipped_items.items():
            if item:
                print(f"{slot.capitalize()}: {item['name']} (Attack Bonus: {item.get('attack_bonus', 0)})")
            else:
                print(f"{slot.capitalize()}: None")
