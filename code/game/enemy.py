import random
from game.utility.utils import print_status

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

def battle_soul_of_zinder(player):
    soul_of_zinder = Enemy("Soul of Zinder", 200, 20)
    print(f"A fearsome enemy, the {soul_of_zinder.name}, blocks your path!")
    print("His health bar is SOO big, it looks like he has overshielding or something...")
    print("Prepare yourself for a challenging battle!")

    while player.is_alive() and soul_of_zinder.is_alive():
        print_status(player, soul_of_zinder)
        choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

        if choice == "a":
            player_damage = player.attack()
            soul_of_zinder.defend(player_damage)
            print(f"{player.name} attacks the {soul_of_zinder.name} for {player_damage} damage.")

            if soul_of_zinder.is_alive():
                enemy_damage = soul_of_zinder.attack()
                player.defend(enemy_damage)
                print(f"The {soul_of_zinder.name} attacks back for {enemy_damage} damage.")

        elif choice == "u":
            player.check_inventory()
            item_to_use = input("Enter the item you want to use (or [cancel] to go back): ").lower()

            if item_to_use == "cancel":
                continue
            player.use_item(item_to_use)

        elif choice == "f":
            print("You fled from the battle!")
            return
        
        else:
            print("Invalid choice. Please try again.")

    if player.is_alive():
        print(f"Congratulations! You defeated the {soul_of_zinder.name}!")
        input(print("You really are the Dark Soul_Z"))
        input(print("Thank for playing. Click ENTER to exit."))
        input()
        quit()

    else:
        print("You lost the battle against the Soul of Zinder!")
