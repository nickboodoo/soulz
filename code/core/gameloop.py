import random
from core.enemy import Enemy
from core.encounterloop import Encounter
from utility.utils import fast_travel


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
                loot_pool = ["Quest Item", "Health Potion", "Gold", "Zinder"]
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
