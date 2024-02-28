import random

class Player:
    MAX_HEALTH = 100
    MIN_HEALTH = 0

    def __init__(self, name):
        self.name = name
        self.health = self.MAX_HEALTH
        self.mana = 50
        self.equipped_items = {"weapon": None, "armor": None}  # Equipped items
        self.inventory = {"gold": 100, "health potion": 2, "mana potion": 1}
        self.enemies_killed = 0
        self.distance_travelled = 0

    def attack(self):
        if self.equipped_items["weapon"]:
            return random.randint(10, 20) + self.equipped_items["weapon"].attack_bonus
        else:
            return random.randint(10, 20)

    def defend(self, damage):
        self.health -= damage
        if self.health < self.MIN_HEALTH:
            self.health = self.MIN_HEALTH

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
        if item in self.inventory:
            if item == "health potion":
                if self.health == self.MAX_HEALTH:
                    print("Your health is already full.")
                else:
                    self.health = min(self.MAX_HEALTH, self.health + 20)  # Ensure health doesn't exceed max health
                    self.remove_from_inventory(item)
                    print(f"You used a health potion and gained 20 health.")
            # Add more items and their effects here if needed
            else:
                print("You cannot use that item.")
        else:
            print("You don't have that item.")

    def view_character_stats(self):
        print("\nCharacter Stats:")
        print(f"Health: {self.health}/{self.MAX_HEALTH}")
        print(f"Mana: {self.mana}/100")
        print("Equipped Items:")
        for slot, item in self.equipped_items.items():
            if item:
                print(f"{slot.capitalize()}: {item.name}")
            else:
                print(f"{slot.capitalize()}: None")

class Item:
    def __init__(self, name, attack_bonus=0, defense_bonus=0):
        self.name = name
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus

def generate_random_weapon():
    weapons = [
        Item("Sword", attack_bonus=5),
        Item("Axe", attack_bonus=8),
        Item("Bow", attack_bonus=6),
        Item("Staff", attack_bonus=7)
    ]
    return random.choice(weapons)

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
    print(f"{player.name} - HP: {'█' * int(player.health / 5)} ({player.health}/{player.MAX_HEALTH})\n")
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
        "mana potion": 30,
        "weapon": 50,
        "armor": 70,
        # Add more items and their prices here
    }
    print("\nWelcome to the store!")
    print("Here are the items available for purchase:")
    for item, price in store_items.items():
        print(f"{item.capitalize()} - {price} gold")

    while True:
        print("Your Gold:", player.inventory["gold"])
        choice = input("Enter the item you want to buy (or [done] to exit): ").lower()
        if choice == "done":
            break
        elif choice in store_items:
            if player.inventory["gold"] >= store_items[choice]:
                player.add_to_inventory(choice)
                player.inventory["gold"] -= store_items[choice]
                print(f"You bought {choice}!")
            else:
                print("You don't have enough gold to buy that.")
        else:
            print("That item is not available in the store.")

def main():
    player_name = input("Enter your name: ")
    print(f"Welcome, {player_name}!")
    player = Player(player_name)

    while player.is_alive():
        choice = input("\nWhat would you like to do? [explore] or [travel to city] or [quit]? ").lower()
        if choice == "explore":
            encounter_chance = random.randint(1, 10)
            if encounter_chance <= 7:
                encounter_enemy(player)
                player.distance_travelled += 1
            else:
                print("You didn't encounter any enemies while exploring.")
                player.distance_travelled += 1
        elif choice == "travel to city":
            travel_to_city(player)
        elif choice == "quit":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
