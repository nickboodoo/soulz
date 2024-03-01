import random
from utility.utils import battle_soul_of_zinder
from core.enemy import Enemy

class Encounter:
    def __init__(self, player):
        self.player = player

    def encounter_enemy(self):
        # Create enemies
        enemies = [
            Enemy("Goblin", 50, 10),
            Enemy("Skeleton", 40, 15),
            Enemy("Orc", 60, 12)
        ]

        # Select random enemy
        enemy = Enemy.create_random_enemy()

        # Display encounter message to player
        print(f"You've encountered a {enemy.name}!")

        # Combat loop
        while self.player.is_alive() and enemy.is_alive():
            self.print_status(enemy)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

            # Attack logic
            if choice == "a":
                player_damage = self.player.attack()
                enemy.defend(player_damage)
                print(f"{self.player.name} attacks the {enemy.name} for {player_damage} damage.")

                if enemy.is_alive():
                    enemy_damage = enemy.attack()
                    self.player.defend(enemy_damage)
                    print(f"The {enemy.name} attacks back for {enemy_damage} damage.")
            
            # Use Item logic
            elif choice == "u":
                self.player.check_inventory()
                item_to_use = input("Enter the item you want to use (or [cancel] to go back): ").lower()

                if item_to_use == "cancel":
                    continue

                self.player.use_item(item_to_use)

            # Flee logic
            elif choice == "f":
                print("You fled from the battle!")
                return
            
            # Input error handling
            else:
                print("Invalid choice. Please try again.")

        # Battle outcome
        if self.player.is_alive():
            print(f"You defeated the {enemy.name}!")
            self.player.enemies_killed += 1

            # Player level-up logic
            if self.player.enemies_killed % 3 == 0:  # Check if the player has defeated a multiple of 3 enemies
                self.player.level_up()  # Level up the player every 3rd enemy defeated

            # Available loot for rewards
            loot_pool = ["Quest Item", "Health Potion", "Gold", "Zinder"]
            loot = random.choice(loot_pool)

            if loot == "Gold":
                gold_amount = random.randint(1, 100)
                self.player.stats["gold"] += gold_amount
                print(f"You found {gold_amount} gold!")

            elif loot == "Quest Item":
                self.player.add_to_inventory("Quest Item") 
                print(f"You found {loot}!")

                for item, quantity in self.player.inventory.items():
                    if item == "Quest Item":
                        if quantity >= 4:
                            print("You've collected all the necessary quest items!")
                            battle_soul_of_zinder(self.player)  # Trigger boss fight with Soul of Zinder

            elif loot == "Zinder":  
                self.player.zinders_collected += 1 # If Zinder is found, increase the Zinders collected
                print(f"You found {loot}! You now have {self.player.zinders_collected} Zinders.")

            else:
                self.player.add_to_inventory(loot)
                print(f"You found {loot}!")

        # Player loses the game
        else:
            print("You lost the battle!")
            print(f"You've killed {self.player.enemies_killed} enemies and travelled {self.player.distance_travelled} mile(s).")
            exit()
