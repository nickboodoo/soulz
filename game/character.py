import random

"""A base class for all characters in the game (both the player and enemies), 
containing common attributes like health, attack power, and basic actions like attack and defend."""

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