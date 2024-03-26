from game_setup import GameSetup


if __name__ == "__main__":

    input("Welcome to Soulz!")

    setup = GameSetup()
    setup.initialize_game_settings("A", "D")
    setup.setup_game()
    setup.initiate_gameplay_loop()

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
    
