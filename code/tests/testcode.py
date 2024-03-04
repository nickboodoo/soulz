import random

class Encounter:
    def __init__(self, player):
        self.player = player

    def encounter_enemy(self, enemy):
        print(f"You've encountered a {enemy.name}!")

        # Combat loop
        while self.player.is_alive() and enemy.is_alive():
            print_status(self.player, enemy)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

            # Attack logic
            if choice == "a":
                player_damage = self.player.attack()
                enemy.defend(player_damage)
                print(f"{self.player.name} attacks the {enemy.name} for {player_damage} damage.")

                if enemy.is_alive():
                    enemy_damage = enemy.attack()
                    self.player.defend(enemy_damage)
                    print(f"The {enemy.name} attacks back for {enemy_damage} damage.")
            
            # Use item logic
            elif choice == "u":
                self.player.check_inventory()
                item_to_use = input("Enter the item you want to use (or [cancel] to go back): ").lower()

                if item_to_use == "cancel":
                    continue

                self.player.use_item(item_to_use)

            # Flee logic
            elif choice == "f":
                print("You fled from the battle!")
                return
            
            else:
                print("Invalid choice. Please try again.")

        if self.player.is_alive():
            print(f"You defeated the {enemy.name}!")
            self.player.enemies_killed += 1

            # Player level-up logic
            if self.player.enemies_killed % 3 == 0:
                self.player.level_up()

            # Available loot for rewards
            loot_pool = ["Quest Item", "Gold", "Zinder"]
            loot = random.choice(loot_pool)

            if loot == "Gold":
                gold_amount = random.randint(1, 100)
                self.player.stats["gold"] += gold_amount
                print(f"You found {gold_amount} gold!")

            elif loot == "Quest Item":
                self.player.add_to_inventory("Quest Item") 
                print(f"You found {loot}!")

                for item, quantity in self.player.inventory.items():
                    if item == "Quest Item":
                        if quantity >= 4:
                            print("You've collected all the necessary quest items!")
                            battle_soul_of_zinder(self.player)  # Trigger boss fight with Soul of Zinder

            elif loot == "Zinder":  
                self.player.zinders_collected += 1 # If Zinder is found, increase the Zinders collected
                print(f"You found {loot}! You now have {self.player.zinders_collected} Zinders.")

            else:
                self.player.add_to_inventory(loot)
                print(f"You found {loot}!")

        # Player loses the game
        else:
            print("You lost the battle!")
            print(f"You've killed {self.player.enemies_killed} enemies and travelled {self.player.distance_travelled} mile(s).")
            exit()

class Enemy:
    ENEMY_TYPES = [
        ("Goblin", 50, 10),
        ("Skeleton", 40, 15),
        ("Orc", 60, 12)
    ]

    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    @classmethod
    def create_random_enemy(cls):
        enemy_data = random.choice(cls.ENEMY_TYPES)
        name, health, attack_power = enemy_data
        return cls(name, health, attack_power)

    def attack(self):
        return random.randint(5, self.attack_power)

    def defend(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0

def battle_soul_of_zinder(player):
    soul_of_zinder = Enemy("Soul of Zinder", 200, 20)
    print(f"A fearsome enemy, the {soul_of_zinder.name}, blocks your path!")
    print("His health bar is SOO big, it looks like he has overshielding or something...")
    print("Prepare yourself for a challenging battle!")

    while player.is_alive() and soul_of_zinder.is_alive():
        print_status(player, soul_of_zinder)
        choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

        if choice == "a":
            player_damage = player.attack()
            soul_of_zinder.defend(player_damage)
            print(f"{player.name} attacks the {soul_of_zinder.name} for {player_damage} damage.")

            if soul_of_zinder.is_alive():
                enemy_damage = soul_of_zinder.attack()
                player.defend(enemy_damage)
                print(f"The {soul_of_zinder.name} attacks back for {enemy_damage} damage.")

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
        print(f"Congratulations! You defeated the {soul_of_zinder.name}!")
        input(print("You really are the Dark Soul_Z"))
        input(print("Thank for playing. Click ENTER to exit."))
        input()
        quit()

    else:
        print("You lost the battle against the Soul of Zinder!")

class Game:
    def __init__(self):
        pass

    def start(self):

        player_name = input("Enter your name: ")

        welcome_messages(player_name)

        player = Player(player_name)
        game_loop = GameLoop(player)
        game_loop.start_loop()

class GameLoop:
    def __init__(self, player):
        self.player = player

    def start_loop(self):
        while self.player.is_alive():
            choice = input("\nWhat would you like to do? [explore] or [fast travel] or [quit]? ").lower()
            if choice == "explore":
                self.explore()
            elif choice == "fast travel":
                fast_travel(self.player)
            elif choice == "quit":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please try again.")
        if not self.player.is_alive():
            print("Game over.")

    def explore(self):
        encounter_chance = random.randint(1, 10)
        if encounter_chance <= 7:
            enemy_battle = Encounter(self.player)
            enemy = Enemy.create_random_enemy()  # Create a random enemy
            enemy_battle.encounter_enemy(enemy)  # Pass the enemy object to encounter_enemy method
        else:
            found_items = random.randint(1, 3)
            for _ in range(found_items):
                loot_pool = ["Quest Item", "Gold", "Zinder"]
                loot = random.choice(loot_pool)
                if loot == "Gold":
                    gold_amount = random.randint(1, 100)
                    self.player.stats["gold"] += gold_amount
                    print(f"You found {gold_amount} gold!")
                elif loot == "Zinder":
                    self.player.zinders_collected += 1
                    print(f"You found {loot}! You now have {self.player.zinders_collected} Zinders.")
                else:
                    self.player.add_to_inventory(loot)
                    print(f"You found {loot}!")


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
        # Apply lifesteal based on the number of Zinders collected
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
        self.base_damage += 5  # Increase base damage on leveling up
        print(f"Congratulations! You've reached level {self.level}. Your base damage has increased.")

### HELPER FUNCTIONS FOR MESSAGES ###

def welcome_messages(player_name):
    print(f"Welcome, {player_name}!")
    input("Press Enter to continue...")

    print("In this world of Lordran_Z, you must collect the four Quest Items.")
    input("Press Enter to continue...")

    print("Once you do, you will be summoned to fight the Dark Soulz Himself! haHA!")
    input("Press Enter to continue...")

# Helper function to show HP bars
def print_status(player, enemy=None):
    print(f"{player.name} - HP: {'█' * int(player.stats['health'] / 5)} ({player.stats['health']}/{player.MAX_HEALTH})\n")

    # Shows enemy health bar ONLY if enemy is present since enemy=None
    if enemy:
        print(f"{enemy.name} - HP: {'█' * int(enemy.health / 5)} ({enemy.health}/100)\n")

# Helper function for one of the player's main menus
def fast_travel(player):
    print("You have arrived at the city.")

    # Display the City Activities menu to the player
    while True:
        print("\nWelcome to the city!")
        print("What would you like to do?")
        print("[b]uy items")
        print("[c]heck inventory")
        print("[u]se item from inventory")
        print("[s]how character stats")
        print("[t]ravel to tavern")
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

        elif choice == "t":

            stay_at_tavern(player)

        elif choice == "l":
            print("You leave the city.")
            break

        else:
            print("Invalid choice. Please try again.")

def stay_at_tavern(player):
    print("You decide to stay at the tavern for a rest.")
    player.stats["health"] = player.MAX_HEALTH  # Fully replenish player's health
    print("Your health has been fully restored.")

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


if __name__ == "__main__":
    game = Game()
    game.start()