# Define the SoulOfZinder class for mini-bosses
class SoulOfZinder(Enemy):
    def __init__(self, name, health, attack_power):
        super().__init__(name, health, attack_power)
        self.loot_pool = ["Quest Item", "Health Potion", "Mana Potion", "Gold"]

    # Method to drop randomized loot
    def drop_loot(self):
        loot_count = random.randint(4, 5)
        loot_collected = []
        for _ in range(loot_count):
            loot = random.choice(self.loot_pool)
            loot_collected.append(loot)
        return loot_collected