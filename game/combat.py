class Combat:
    def __init__(self, player):
        self.player = player

    def initiate_attack(self, attacker, defender):
        damage = attacker.attack()
        defender.defend(damage)
        print(f"{attacker.name} attacks {defender.name} for {damage} damage.".center(72))

    def check_alive(self, character):
        return character.is_alive()