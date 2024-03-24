import random
from game.utilities.utils import clear_screen, fast_travel
from game.sequence_loops.battle_manager import BattleManager
from game.characters.enemy import Enemy
from game.utilities.boss_battle import BossBattle


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