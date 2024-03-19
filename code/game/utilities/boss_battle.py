from game.characters.enemy import Enemy
from game.utilities.utils import print_status


class BossBattle:
    def __init__(self, player):
        self.player = player
        self.soul_of_zinder = Enemy("Soul of Zinder", 100, 55)

    def battle_soul_of_zinder(self):
        print(f"The {self.soul_of_zinder.name} appears!")
        input("Prepare yourself for a challenging battle!")

        while self.player.is_alive() and self.soul_of_zinder.is_alive():
            print_status(self.player, self.soul_of_zinder)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

            if choice == "a":
                player_damage = self.player.attack()
                self.soul_of_zinder.defend(player_damage)
                print(f"{self.player.name} attacks the {self.soul_of_zinder.name} for {player_damage} damage.")

                if self.soul_of_zinder.is_alive():
                    enemy_damage = self.soul_of_zinder.attack()
                    self.player.defend(enemy_damage)
                    print(f"The {self.soul_of_zinder.name} attacks back for {enemy_damage} damage.")

            elif choice == "u":
                self.player.check_inventory()
                item_to_use = input("Enter the item you want to use (or [cancel] to go back): ").lower()

                if item_to_use == "cancel":
                    continue
                self.player.use_item(item_to_use)

            elif choice == "f":
                print("You fled from the battle!")
                return
            
            else:
                print("Invalid choice. Please try again.")

        if self.player.is_alive():
            print(f"Congratulations! You defeated the {self.soul_of_zinder.name}!")
            input("Thank for playing. Click ENTER to exit.")
            quit()

        else:
            print("You lost the battle against the Soul of Zinder!")
