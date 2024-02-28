import random

class Player:
    MAX_HEALTH = 100
    MIN_HEALTH = 0

    def __init__(self, name):
        self.name = name
        self.stats = {"health": self.MAX_HEALTH, "gold": 100}
        self.level = 1
        self.base_damage = 10  # Base damage
        self.inventory = {"health potion": 2}
        self.enemies_killed = 0
        self.distance_travelled = 0
        self.encounters = []
        self.quest_items_collected = set()

    def attack(self):
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
        self.base_damage += 5  # Increase base damage on leveling up
        print(f"Congratulations! You've reached level {self.level}. Your base damage has increased.")

class Enemy:
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

def print_status(player, enemy=None):
    print(f"{player.name} - HP: {'█' * int(player.stats['health'] / 5)} ({player.stats['health']}/{player.MAX_HEALTH})\n")
    if enemy:
        print(f"{enemy.name} - HP: {'█' * int(enemy.health / 5)} ({enemy.health}/100)\n")

def encounter_enemy(player):
    enemies = [
        Enemy("Goblin", 50, 10),
        Enemy("Skeleton", 40, 15),
        Enemy("Orc", 60, 12)
    ]
    enemy = random.choice(enemies)
    print(f"You've encountered a {enemy.name}!")
    player.encounters.append(enemy.name)

    while player.is_alive() and enemy.is_alive():
        print_status(player, enemy)
        choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

        if choice == "a":
            player_damage = player.attack()
            enemy.defend(player_damage)
            print(f"{player.name} attacks the {enemy.name} for {player_damage} damage.")
            if enemy.is_alive():
                enemy_damage = enemy.attack()
                player.defend(enemy_damage)
                print(f"The {enemy.name} attacks back for {enemy_damage} damage.")
        elif choice == "u":
            player.check_inventory()
            item_to_use = input("Enter the item you want to use (or [cancel] to go back): ").lower()
            if item_to_use == "cancel":
                continue
            player.use_item(item_to_use)
        elif choice == "f":
            print("You fled from the battle!")
            return
        else:
            print("Invalid choice. Please try again.")

    if player.is_alive():
        print(f"You defeated the {enemy.name}!")
        player.enemies_killed += 1
        loot_pool = ["Quest Item", "Health Potion", "Gold"]
        loot = random.choice(loot_pool)
        if loot == "Gold":
            gold_amount = random.randint(1, 100)
            player.stats["gold"] += gold_amount
            print(f"You found {gold_amount} gold!")
        else:
            player.add_to_inventory(loot)
            print(f"You found {loot}!")
    else:
        print("You lost the battle!")
        print(f"You've killed {player.enemies_killed} enemies and travelled {player.distance_travelled} miles.")
        exit()

def travel_to_city(player):
    print("You have arrived at the city.")
    while True:
        print("\nWelcome to the city!")
        print("What would you like to do?")
        print("[b]uy items")
        print("[c]heck inventory")
        print("[u]se item from inventory")
        print("[s]how character stats")
        print("[l]eave city")
        choice = input("Enter your choice: ").lower()
        if choice == "b":
            buy_items(player)
        elif choice == "c":
            player.check_inventory()
        elif choice == "u":
            item_to_use = input("Enter the item you want to use from your inventory: ").lower()
            player.use_item(item_to_use)
        elif choice == "s":
            player.view_character_stats()
        elif choice == "l":
            print("You leave the city.")
            break
        else:
            print("Invalid choice. Please try again.")

def buy_items(player):
    store_items = {
        "health potion": 20,
    }
    print("\nWelcome to the store!")
    print("Here are the items available for purchase:")
    for item, price in store_items.items():
        print(f"{item.capitalize()} - {price} gold")

    while True:
        print("Your Gold:", player.stats["gold"])
        choice = input("Enter the item you want to buy (or [done] to exit): ").lower()
        if choice == "done":
            break
        elif choice in store_items:
            if player.stats["gold"] >= store_items[choice]:
                player.add_to_inventory(choice)
                player.stats["gold"] -= store_items[choice]
                print(f"You bought {choice}!")
            else:
                print("You don't have enough gold to buy that.")
        else:
            print("That item is not available in the store.")

class Game:
    def __init__(self):
        pass

    def start(self):
        player_name = input("Enter your name: ")
        print(f"Welcome, {player_name}!")
        input()
        print("In this world of Lordran_Z, you must slay the four Soulz of Sinders.")
        input()
        print("Once you do, you will be summoned to fight the Dark Soulz Himself! haHA!")
        input()
        player = Player(player_name)

        while player.is_alive():
            choice = input("\nWhat would you like to do? [explore] or [travel to city] or [quit]? ").lower()
            if choice == "explore":
                encounter_chance = random.randint(1, 10)
                if encounter_chance <= 7:
                    encounter_enemy(player)
                else:
                    found_items = random.randint(1, 3)
                    for _ in range(found_items):
                        loot_pool = ["Quest Item", "Health Potion", "Gold"]
                        loot = random.choice(loot_pool)
                        if loot == "Gold":
                            gold_amount = random.randint(1, 100)
                            player.stats["gold"] += gold_amount
                            print(f"You found {gold_amount} gold!")
                        else:
                            player.add_to_inventory(loot)
                            print(f"You found {loot}!")
            elif choice == "travel to city":
                travel_to_city(player)
            elif choice == "quit":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please try again.")

        if not player.is_alive():
            print("Game over.")

if __name__ == "__main__":
    game = Game()
    game.start()
