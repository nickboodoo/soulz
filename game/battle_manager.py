import math
import random
from combat import Combat
from utils import clear_screen, print_dashes, print_status

"""Manages combat encounters between the player and enemies.
It handles the flow of battle, including making choices like attacking, using items, or fleeing."""

class BattleManager(Combat):
    def __init__(self, player):
        super().__init__(player)

    def start_battle(self, enemy):
        self.clear_screen()
        print_dashes(72)
        print(f"You've encountered a {enemy.name}!".center(72))

        while self.check_alive(self.player) and self.check_alive(enemy):
            print_dashes(72)
            print_status(self.player, enemy)
            print_dashes(72)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()
            self.clear_screen()

            if choice == "a":
                self.initiate_attack(self.player, enemy)
                if self.check_alive(enemy):
                    self.initiate_attack(enemy, self.player)
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
        clear_screen()

        if item_to_use != "cancel":
            self.player.use_item(item_to_use)

    def handle_battle_outcome(self, enemy):
        if self.player.is_alive():
            self.player_victory(enemy)
        else:
            self.player_defeat()

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
        loot_pool = ["Gold", "Zinder"]
        return random.choice(loot_pool)

    def handle_loot(self, loot):
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