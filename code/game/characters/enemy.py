import random
from game.characters.character import Character


class Enemy(Character):
    def __init__(self, name, health, attack_power):
        super().__init__(name, health, attack_power)

    @classmethod
    def create_random_enemy(cls):
        enemy_types = [
            ("Random Enemy 1", 50, 15),
            ("Random Enemy 2", 60, 12),
            ("Random Enemy 3", 40, 20),
        ]
        name, health, attack_power = random.choice(enemy_types)
        return cls(name, health, attack_power)