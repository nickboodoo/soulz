import random
from game.utils import fast_travel

from game.battle_manager import BattleManager

from game.enemy import Enemy

from game.boss_battle import BossBattle


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