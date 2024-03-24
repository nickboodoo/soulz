


class GameLoop:
    def __init__(self, player, world_state):
        self.player = player
        self.world_state = world_state

    def start_loop(self):
        while self.player.is_alive():
            choice = input("\nWhat would you like to do? [explore] or [fast travel] or [quit]? ").lower()
            clear_screen()

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

    # OVERHAUL THIS CONCEPT
    def explore(self):
        encounter_chance = random.randint(1, 10)

        if encounter_chance <= 7:
            enemy_battle = BattleManager(self.player)
            enemy = Enemy.create_random_enemy()
            enemy_battle.start_battle(enemy)

        else:
            found_items = random.randint(1, 3)

            for _ in range(found_items):
                loot_pool = ["Ancient Runestone", "Gold", "Zinder"]
                loot = random.choice(loot_pool)

                if loot == "Gold":
                    gold_amount = random.randint(1, 100)
                    self.player.stats["gold"] += gold_amount
                    input(f"You found {gold_amount} gold!")

                elif loot == "Zinder":
                    self.player.zinders_collected += 1
                    input(f"You found {loot}! You now have {self.player.zinders_collected} Zinders.")

                else:
                    self.player.add_to_inventory(loot)
                    input(f"You found {loot}!")

            if "Ancient Runestone" in self.player.inventory and self.player.inventory["Ancient Runestone"] >= 4:
                final_boss_battle = BossBattle(self.player)
                final_boss_battle.battle_soul_of_zinder()



# SOME OF THESE SHOULD BE @STATICMETHODS IN PLAYER CLASS

import math
import os
import random

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_dashes(x):
    dash = '-'
    border = dash * x
    print(border)

def print_status(player, enemy=None):
    print(f"{player.name} - HP: {'█' * int(player.health / 5)} ({player.health}/{player.MAX_HEALTH})\n".rjust(72))
    if enemy:
        print(f"{enemy.name} - HP: {'█' * int(enemy.health / 5)} ({enemy.health}/100)\n".rjust(72))

def fast_travel(player):
    print("You have arrived at the city.")
    while True:
        print_city_menu()
        choice = input("Enter your choice: ").lower()
        clear_screen()
        if choice == "b":
            buy_items(player)
        elif choice == "c":
            player.check_inventory()
        elif choice == "u":
            player.check_inventory()
            item_to_use = input("Enter the item you want to use from your inventory: ").lower()
            clear_screen()
            player.use_item(item_to_use)
        elif choice == "s":
            player.view_character_stats()
        elif choice == "t":
            stay_at_tavern(player)
        elif choice == "l":
            input("You leave the city.")
            clear_screen()
            break
        else:
            print("Invalid choice. Please try again.")

def stay_at_tavern(player):
    print("You decide to stay at the tavern for a rest.")
    player.health = player.MAX_HEALTH
    input("Your health has been fully restored.")
    clear_screen()

def buy_items(player):
    store_items = {
        "health potion": 20,
    }
    print("\nWelcome to the store!")
    print("Here are the items available for purchase:")
    
    while True:
        print("Your Gold:", player.stats["gold"])

        for item, price in store_items.items():
            print(f"{item.capitalize()} - {price} gold")

        choice = input("Enter the item you want to buy (or [done] to exit): ").lower()
        clear_screen()

        if choice == "done":
            break

        elif choice in store_items:

            if player.stats["gold"] >= store_items[choice]:
                player.add_to_inventory(choice)
                player.stats["gold"] -= store_items[choice]
                input(f"You bought {choice}!")
                clear_screen()

            else:
                input("You don't have enough gold to buy that.")
                clear_screen()

        else:
            input("That item is not available in the store.")
            clear_screen()

def print_city_menu():
        print("\nWelcome to the city!")
        print("What would you like to do?")
        print("[b]uy items")
        print("[c]heck inventory")
        print("[u]se item from inventory")
        print("[s]how character stats")
        print("[t]ravel to tavern")
        print("[l]eave city")

import random

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

    def use_item(self, item):
        if item in self.inventory and self.inventory[item] > 0:

            if item == "health potion":

                if self.health == self.MAX_HEALTH:
                    input("Your health is already full.")

                else:
                    heal_amount = 20
                    self.health = min(self.MAX_HEALTH, self.health + heal_amount)
                    self.inventory[item] -= 1
                    input(f"You used a health potion and gained {heal_amount} health.")
            else:
                input("You cannot use that item.")

        else:
            input("You don't have that item or you've run out.")

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

class Game:
    def __init__(self):
        pass

    def start(self):

        player_name = input("Enter your name: ")

        print_welcome_messages(player_name)

        player = Player(player_name)
        game_loop = GameLoop(player)
        game_loop.start_loop()

class BossBattle:
    def __init__(self, player):
        self.player = player
        self.soul_of_zinder = Enemy("Soul of Zinder", 100, 55)

    def battle_soul_of_zinder(self):
        print(f"The {self.soul_of_zinder.name} appears!")
        input("Prepare yourself for a challenging battle!")

        while self.player.is_alive() and self.soul_of_zinder.is_alive():
            print_status(self.player, self.soul_of_zinder)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

            if choice == "a":
                player_damage = self.player.attack()
                self.soul_of_zinder.defend(player_damage)
                print(f"{self.player.name} attacks the {self.soul_of_zinder.name} for {player_damage} damage.")

                if self.soul_of_zinder.is_alive():
                    enemy_damage = self.soul_of_zinder.attack()
                    self.player.defend(enemy_damage)
                    print(f"The {self.soul_of_zinder.name} attacks back for {enemy_damage} damage.")

            elif choice == "u":
                self.player.check_inventory()
                item_to_use = input("Enter the item you want to use (or [cancel] to go back): ").lower()

                if item_to_use == "cancel":
                    continue
                self.player.use_item(item_to_use)

            elif choice == "f":
                print("You fled from the battle!")
                return
            
            else:
                print("Invalid choice. Please try again.")

        if self.player.is_alive():
            print(f"Congratulations! You defeated the {self.soul_of_zinder.name}!")
            input("Thank for playing. Click ENTER to exit.")
            quit()

        else:
            print("You lost the battle against the Soul of Zinder!")


class BattleManager:
    def __init__(self, player):
        self.player = player

    def start_battle(self, enemy):
        print_dashes(72)
        print(f"You've encountered a {enemy.name}!".center(72))

        while self.player.is_alive() and enemy.is_alive():
            print_dashes(72)
            print_status(self.player, enemy)
            print_dashes(72)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()
            clear_screen()

            if choice == "a":
                self.player_attack(enemy)
                if enemy.is_alive():
                    self.enemy_attack(enemy)
                else:
                    print_dashes(72)
                    print_status(self.player, enemy)
                    print_dashes(72)
            
            elif choice == "u":
                self.player_use_item()

            elif choice == "f":
                clear_screen()

                print("You fled from the battle!")
                return
            
            else:
                print("Invalid choice. Please try again.")

        self.handle_battle_outcome(enemy)

    def player_attack(self, enemy):
        print_dashes(72)
        player_damage = self.player.attack()
        enemy.defend(player_damage)
        print(f"{self.player.name} attacks the {enemy.name} for {player_damage} damage.".center(72))

    def enemy_attack(self, enemy):
        enemy_damage = enemy.attack()
        self.player.defend(enemy_damage)
        print(f"The {enemy.name} attacks back for {enemy_damage} damage.".center(72))

    def player_use_item(self):
        self.player.check_inventory()
        item_to_use = input("Enter the item you want to use (or [cancel] to go back): ").lower()

        if item_to_use != "cancel":
            self.player.use_item(item_to_use)

    def handle_battle_outcome(self, enemy):
        if self.player.is_alive():
            self.player_victory(enemy)
        else:
            self.player_defeat(enemy)

    def player_victory(self, enemy):
        print(f"You defeated the {enemy.name}!")
        self.player.enemies_killed += 1

        required_kills = math.ceil(math.log(self.player.level + 1, 2) * 3)
        if self.player.enemies_killed >= required_kills:
            self.player.level_up()
            self.player.enemies_killed = 0

        loot = self.generate_loot()
        self.handle_loot(loot)

    def player_defeat(self):
        input("You lose!")
        exit()

    def generate_loot(self):
        loot_pool = ["Ancient Runestone", "Gold", "Zinder"]
        return random.choice(loot_pool)

    def handle_loot(self, loot):
        if loot == "Gold":
            gold_amount = random.randint(1, 100)
            self.player.stats["gold"] += gold_amount
            input(f"You found {gold_amount} gold!")

        elif loot == "Ancient Runestone":
            self.player.add_to_inventory("Ancient Runestone") 
            input(f"You found an {loot}!")

            for item, quantity in self.player.inventory.items():

                if item == "Ancient Runestone" and quantity >= 10:
                    input("You've collected enough runestones to draw the attention of something terrifying!")
                    
        elif loot == "Zinder":  
            self.player.zinders_collected += 1
            input(f"You found {loot}! You now have {self.player.zinders_collected} Zinders.")

        else:
            self.player.add_to_inventory(loot)
            input(f"You found {loot}!")

player_name = input("Enter your name: ")
player = Player(player_name)


game_loop = GameLoop(player, world_state)


game_loop.start_loop()