import random
from .player import Player
from .enemy import Enemy
from .utils import encounter_enemy, travel_to_city

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
                    print("You didn't encounter any enemies while exploring.")
            elif choice == "travel to city":
                travel_to_city(player)
            elif choice == "quit":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please try again.")
