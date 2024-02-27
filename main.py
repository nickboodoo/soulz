import random

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.attack = 10
        self.defense = 5

    def take_damage(self, damage):
        self.hp -= damage

    def attack_enemy(self, enemy):
        damage = random.randint(0, self.attack)
        enemy.take_damage(damage)

class Enemy:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = 0  # Add a default defense attribute

    def take_damage(self, damage):
        self.hp -= max(0, damage - self.defense)


    def attack_player(self, player):
        damage = random.randint(0, self.attack)
        player.take_damage(damage)

class Game:
    def __init__(self):
        self.player = Player("Hero")
        self.enemies = [Enemy("Skeleton", 50, 5), Enemy("Zombie", 80, 8)]
        self.level = 1

    def play(self):
        print("Welcome to Text-Based RPG!")
        while self.player.hp > 0:
            print(f"Level {self.level}")
            self.encounter()
            self.level += 1
        print("Game Over")

    def encounter(self):
        enemy = random.choice(self.enemies)
        print(f"You encountered a {enemy.name}!")
        while enemy.hp > 0 and self.player.hp > 0:
            print(f"{self.player.name} HP: {self.player.hp}")
            print(f"{enemy.name} HP: {enemy.hp}")
            action = input("What will you do? (attack/flee): ")
            print("---------------------------------------------")
            if action == "attack":
                self.player.attack_enemy(enemy)
                if enemy.hp <= 0:
                    print(f"You defeated the {enemy.name}!")
                    print("---------------------------------------------")
                    break
                enemy.attack_player(self.player)
            elif action == "flee":
                print("You ran away!")
                print("---------------------------------------------")
                break
            else:
                print("Invalid action!")

# Main
if __name__ == "__main__":
    game = Game()
    game.play()
