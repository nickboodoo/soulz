import random

class Enemy:
    ENEMY_TYPES = [
        ("Goblin", 50, 10),
        ("Skeleton", 40, 15),
        ("Orc", 60, 12)
    ]

    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    @classmethod
    def create_random_enemy(cls):
        enemy_data = random.choice(cls.ENEMY_TYPES)
        name, health, attack_power = enemy_data
        return cls(name, health, attack_power)

    def attack(self):
        return random.randint(5, self.attack_power)

    def defend(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0
