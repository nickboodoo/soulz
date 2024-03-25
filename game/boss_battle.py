from enemy import Enemy
from combat import Combat
from utils import clear_screen, print_status

"""A specialized battle class for significant, challenging encounters against a boss enemy. 
It includes unique dialogues and battle mechanics."""

class BossBattle(Combat):
    def __init__(self, player):
        super().__init__(player)
        self.soul_of_zinder = Enemy("Soul of Zinder", 100, 55)  # Assuming Enemy class definition

    def battle_soul_of_zinder(self):
        clear_screen()
        print(f"The {self.soul_of_zinder.name} appears!")
        input("Prepare yourself for a challenging battle!")

        while self.check_alive(self.player) and self.check_alive(self.soul_of_zinder):
            print_status(self.player, self.soul_of_zinder)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

            if choice == "a":
                self.initiate_attack(self.player, self.soul_of_zinder)
                if self.check_alive(self.soul_of_zinder):
                    self.initiate_attack(self.soul_of_zinder, self.player)

            elif choice == "u":
                self.player.check_inventory()
                item_to_use = input("Enter the item you want to use (or [cancel] to go back): ").lower()
                clear_screen()

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