import random

from game.gameloop import GameLoop
from .player import Player
from .utils import encounter_enemy, travel_to_city, battle_soul_of_zinder
from game.lore import Lore



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
        game_loop = GameLoop(player)
        game_loop.start_loop()
