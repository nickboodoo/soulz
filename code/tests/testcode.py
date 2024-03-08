import random


#-----------------------------------------------#
#                CLASS BOSSBATTLE               #
#-----------------------------------------------#

class BossBattle:
    def __init__(self, player):
        self.player = player
        self.soul_of_zinder = Enemy("Soul of Zinder", 200, 20)

    def battle_soul_of_zinder(self):
        soul_of_zinder = Enemy("Soul of Zinder", 200, 20)
        print(f"A fearsome enemy, the {soul_of_zinder.name}, blocks your path!")
        print("His health bar is SOO big, it looks like he has overshielding or something...")
        print("Prepare yourself for a challenging battle!")

        while self.player.is_alive() and soul_of_zinder.is_alive():
            print_status(self.player, soul_of_zinder)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

            if choice == "a":
                player_damage = self.player.attack()
                soul_of_zinder.defend(player_damage)
                print(f"{self.player.name} attacks the {soul_of_zinder.name} for {player_damage} damage.")

                if soul_of_zinder.is_alive():
                    enemy_damage = soul_of_zinder.attack()
                    self.player.defend(enemy_damage)
                    print(f"The {soul_of_zinder.name} attacks back for {enemy_damage} damage.")

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
            print(f"Congratulations! You defeated the {soul_of_zinder.name}!")
            print("You really are the Dark Soul_Z")
            print("Thank for playing. Click ENTER to exit.")
            input()
            quit()

        else:
            print("You lost the battle against the Soul of Zinder!")

#-----------------------------------------------#
#             CLASS  BATTLEMANAGER              #
#-----------------------------------------------#

class BattleManager:
    def __init__(self, player):
        self.player = player

    def start_battle(self, enemy):
        print(f"You've encountered a {enemy.name}!")

        while self.player.is_alive() and enemy.is_alive():
            print_status(self.player, enemy)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

            if choice == "a":
                self.player_attack(enemy)
                if enemy.is_alive():
                    self.enemy_attack(enemy)
            
            elif choice == "u":
                self.player_use_item()

            elif choice == "f":
                print("You fled from the battle!")
                return
            
            else:
                print("Invalid choice. Please try again.")

        self.handle_battle_outcome(enemy)

    def player_attack(self, enemy):
        player_damage = self.player.attack()
        enemy.defend(player_damage)
        print(f"{self.player.name} attacks the {enemy.name} for {player_damage} damage.")

    def enemy_attack(self, enemy):
        enemy_damage = enemy.attack()
        self.player.defend(enemy_damage)
        print(f"The {enemy.name} attacks back for {enemy_damage} damage.")

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

        if self.player.enemies_killed % 3 == 0:
            self.player.level_up()

        loot = self.generate_loot()
        self.handle_loot(loot)

    def player_defeat(self, enemy):
        print("You lost the battle!")
        print(f"You've killed {self.player.enemies_killed} enemies and travelled {self.player.distance_travelled} mile(s).")
        exit()

    def generate_loot(self):
        loot_pool = ["Quest Item", "Gold", "Zinder"]
        return random.choice(loot_pool)

    def handle_loot(self, loot):
        if loot == "Gold":
            gold_amount = random.randint(1, 100)
            self.player.stats["gold"] += gold_amount
            print(f"You found {gold_amount} gold!")

        elif loot == "Quest Item":
            self.player.add_to_inventory("Quest Item") 
            print(f"You found {loot}!")

            for item, quantity in self.player.inventory.items():
                if item == "Quest Item" and quantity >= 4:
                    world_state.notify_boss_fight_requirement()
                    print("You've collected all the necessary quest items!")
                    

        elif loot == "Zinder":  
            self.player.zinders_collected += 1
            print(f"You found {loot}! You now have {self.player.zinders_collected} Zinders.")

        else:
            self.player.add_to_inventory(loot)
            print(f"You found {loot}!")

#-----------------------------------------------#
#                 CLASS CHARACTER               #
#-----------------------------------------------#

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

#-----------------------------------------------#
#                CLASS PLAYER                   #
#-----------------------------------------------#

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


#-----------------------------------------------#
#                CLASS  ENEMY                   #
#-----------------------------------------------#

class Enemy(Character):
    def __init__(self, name, health, attack_power):
        super().__init__(name, health, attack_power)

    @classmethod  # This decorator was missing
    def create_random_enemy(cls):
        enemy_types = [
            ("Random Enemy 1", 50, 15),
            ("Random Enemy 2", 60, 12),
            ("Random Enemy 3", 40, 20),
        ]
        name, health, attack_power = random.choice(enemy_types)
        return cls(name, health, attack_power)


#-----------------------------------------------#
#                 CLASS GAME                    #
#-----------------------------------------------#

class Game:
    def __init__(self):
        pass

    def start(self):

        player_name = input("Enter your name: ")

        welcome_messages(player_name)

        player = Player(player_name)
        game_loop = GameLoop(player)
        game_loop.start_loop()

#-----------------------------------------------#
#               CLASS GAMELOOP                  #
#-----------------------------------------------#


class GameLoop:
    def __init__(self, player, world_state):
        self.player = player
        self.world_state = world_state  # Now correctly storing the passed world_state



    # Adjustments in the explore method and others as necessary to use world_state

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
            enemy_battle = BattleManager(self.player)
            enemy = Enemy.create_random_enemy()
            enemy_battle.start_battle(enemy)
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

            if "Quest Item" in self.player.inventory and self.player.inventory["Quest Item"] >= 4:
                # Trigger final boss battle when player has collected all quest items
                final_boss_battle = BossBattle(self.player)
                final_boss_battle.battle_soul_of_zinder()




def print_status(player, enemy=None):
    # Updated to use player.health directly instead of player.stats['health']
    print(f"{player.name} - HP: {'█' * int(player.health / 5)} ({player.health}/{player.MAX_HEALTH})\n")
    if enemy:
        print(f"{enemy.name} - HP: {'█' * int(enemy.health / 5)} ({enemy.health}/100)\n")


def fast_travel(player):
    print("You have arrived at the city.")
    while True:
        print_city_menu()
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
    player.health = player.MAX_HEALTH  # Directly set player's health to MAX_HEALTH
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

def print_city_menu():
        print("\nWelcome to the city!")
        print("What would you like to do?")
        print("[b]uy items")
        print("[c]heck inventory")
        print("[u]se item from inventory")
        print("[s]how character stats")
        print("[t]ravel to tavern")
        print("[l]eave city")

def welcome_messages(player_name):
    print(f"Welcome, {player_name}!")
    input("Press Enter to continue...")
    print("In this world of Lordran_Z, you must collect the four Quest Items.")
    input("Press Enter to continue...")
    print("Once you do, you will be summoned to fight the Dark Soulz Himself! haHA!")
    input("Press Enter to continue...")

#-----------------------------------------------#
#             CLASS   WORLDSTATES               #
#-----------------------------------------------#

class WorldStates:
    def __init__(self):
        pass

    def notify_boss_fight_requirement(self):
        print("You have fulfilled the requirements to challenge the Boss!")
        print("Prepare yourself for the ultimate battle!")

if __name__ == "__main__":
    world_state = WorldStates()
    player_name = input("Enter your name: ")
    player = Player(player_name)
    game_loop = GameLoop(player, world_state)
    game_loop.start_loop()


# Remove quit() and exit(), and replace with a control flow that checks game state.