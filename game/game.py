import random
from .player import Player
from .utils import encounter_enemy, travel_to_city, battle_soul_of_zinder

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
                        loot_pool = ["Quest Item", "Health Potion", "Gold", "Zinder"]  # Include Zinder in loot pool
                        loot = random.choice(loot_pool)
                        if loot == "Gold":
                            gold_amount = random.randint(1, 100)
                            player.stats["gold"] += gold_amount
                            print(f"You found {gold_amount} gold!")
                        elif loot == "Zinder":  # If Zinder is found, increase the Zinders collected
                            player.zinders_collected += 1
                            print(f"You found {loot}! You now have {player.zinders_collected} Zinders.")
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