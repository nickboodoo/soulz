import random

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

class Enemy(Character):
    def __init__(self, name, health, attack_power):
        super().__init__(name, health, attack_power)

    @classmethod
    def create_random_enemy(cls):
        enemy_types = [
            ("Abyssal Revenant", 50, 25),
            ("Crimson Shade", 60, 22),
            ("Dreadbone Wraith", 35, 30),
            ("Spectral Sentinel", 80, 15),
            ("Netherghast Fiend", 40, 20),
            ("Voidborne Behemoth", 100, 17),
            ("Rimefrost Phantom", 65, 18),
            ("Shadowveil Assassin", 45, 25),
            ("Infernal Chimera", 90, 22),
            ("Searing Phoenix", 70, 22),
            ("Eldritch Gorgon", 85, 35),
        ]
        
        name, health, attack_power = random.choice(enemy_types)
        return cls(name, health, attack_power)

class Player(Character):
    MAX_HEALTH = 100
    MIN_HEALTH = 0

    def __init__(self, name):
        super().__init__(name, self.MAX_HEALTH, 10)
        self.stats = {"gold": 100}
        self.inventory = {}
        self.enemies_killed = 0
        self.zinders_collected = 0
        self.base_damage = 10
        self.level = 1

    def level_up(self):
        self.level += 1
        self.base_damage += 5
        input(f"Congratulations! You've reached level {self.level}. Your base damage has increased.")

    def attack(self):
        lifesteal_percentage = self.zinders_collected * 0.01
        lifesteal_amount = int(self.base_damage * lifesteal_percentage)
        self.health += lifesteal_amount
        self.health = min(self.MAX_HEALTH, self.health)
        return random.randint(self.base_damage, self.base_damage + 10)

    def defend(self, damage):
        self.health = max(self.MIN_HEALTH, self.health - damage)

    def is_alive(self):
        return self.health > self.MIN_HEALTH

    def add_to_inventory(self, item, quantity=1):
        if item in self.inventory:
            self.inventory[item] += quantity

        else:
            self.inventory[item] = quantity

    def remove_from_inventory(self, item, quantity=1):
        if item in self.inventory:

            if self.inventory[item] >= quantity:

                self.inventory[item] -= quantity
                return True
            
        return False

    def check_inventory(self):
        print("\nInventory:")

        for item, quantity in self.inventory.items():
            print(f"{item.capitalize()}: {quantity}")

    def use_item(self, item):
        if item in self.inventory and self.inventory[item] > 0:

            if item == "health potion":

                if self.health == self.MAX_HEALTH:
                    input("Your health is already full.")

                else:
                    heal_amount = 20
                    self.health = min(self.MAX_HEALTH, self.health + heal_amount)
                    self.inventory[item] -= 1
                    input(f"You used a health potion and gained {heal_amount} health.")
            else:
                input("You cannot use that item.")

        else:
            input("You don't have that item or you've run out.")

    def print_attack_info(lifesteal_percentage, base_damage):
        print(f"Current lifesteal: {lifesteal_percentage*100:.0f}% \nBase damage range: {base_damage} - {base_damage + 10}.")

    def view_character_stats(self):
        lifesteal_percentage = self.zinders_collected * 0.01
        print("\nCharacter Stats:")
        print(f"Health: {self.health}/{self.MAX_HEALTH}")
        print(f"Level: {self.level}")
        print(f"Current lifesteal: {lifesteal_percentage*100:.0f}%")
        print(f"Attack damage range: {self.base_damage} - {self.base_damage + 10}")

    def level_up(self):
        self.level += 1
        self.base_damage += 5
        input(f"Congratulations! You've reached level {self.level}. Your base damage has increased.")