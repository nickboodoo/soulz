import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = {"gold": 100}

    def attack(self):
        return random.randint(10, 20)

    def defend(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0

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
    print(f"{player.name} - HP: {'█' * int(player.health / 5)} ({player.health}/100)\n")
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
            print("Inventory:")
            for item, quantity in player.inventory.items():
                print(f"{item}: {quantity}")
            item_to_use = input("Enter the item you want to use: ").lower()
            if item_to_use in player.inventory:
                if item_to_use == "health potion":
                    if player.health == 100:
                        print("Your health is already full.")
                    else:
                        player.health += 20  # Example: Health potion adds 20 HP
                        player.remove_from_inventory(item_to_use)
                        print(f"You used a health potion and gained 20 health.")
                # Add more items and their effects here if needed
                else:
                    print("You cannot use that item in combat.")
            else:
                print("You don't have that item.")
        elif choice == "f":
            print("You fled from the battle!")
            return
        else:
            print("Invalid choice. Please try again.")

    if player.is_alive():
        print(f"You defeated the {enemy.name}!")
        loot = random.choice(["health potion", "mana potion", "gold"])
        print(f"You found a {loot}!")
        player.add_to_inventory(loot)
    else:
        print("Game Over!")

def travel_to_city(player):
    print("You have arrived at the city.")
    while True:
        print("\nWelcome to the city!")
        print("What would you like to do?")
        print("[b]uy items")
        print("[l]eave city")
        choice = input("Enter your choice: ").lower()
        if choice == "b":
            buy_items(player)
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
            else:
                print("You didn't encounter any enemies while exploring.")
        elif choice == "travel to city":
            travel_to_city(player)
        elif choice == "quit":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
