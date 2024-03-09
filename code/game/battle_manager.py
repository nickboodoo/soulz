import random
from game.world_states import WorldStates
from game.utils import print_status


class BattleManager:
    def __init__(self, player):
        self.player = player

    def start_battle(self, enemy):
        print(f"You've encountered a {enemy.name}!")

        while self.player.is_alive() and enemy.is_alive():
            print_status(self.player, enemy)
            choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

            if choice == "a":
                self.player_attack(enemy)
                if enemy.is_alive():
                    self.enemy_attack(enemy)
            
            elif choice == "u":
                self.player_use_item()

            elif choice == "f":
                print("You fled from the battle!")
                return
            
            else:
                print("Invalid choice. Please try again.")

        self.handle_battle_outcome(enemy)

    def player_attack(self, enemy):
        player_damage = self.player.attack()
        enemy.defend(player_damage)
        print(f"{self.player.name} attacks the {enemy.name} for {player_damage} damage.")

    def enemy_attack(self, enemy):
        enemy_damage = enemy.attack()
        self.player.defend(enemy_damage)
        print(f"The {enemy.name} attacks back for {enemy_damage} damage.")

    def player_use_item(self):
        self.player.check_inventory()
        item_to_use = input("Enter the item you want to use (or [cancel] to go back): ").lower()

        if item_to_use != "cancel":
            self.player.use_item(item_to_use)

    def handle_battle_outcome(self, enemy):
        if self.player.is_alive():
            self.player_victory(enemy)
        else:
            self.player_defeat(enemy)

    def player_victory(self, enemy):
        print(f"You defeated the {enemy.name}!")
        self.player.enemies_killed += 1

        if self.player.enemies_killed % 3 == 0:
            self.player.level_up()

        loot = self.generate_loot()
        self.handle_loot(loot)

    def player_defeat(self, enemy):
        print("You lost the battle!")
        print(f"You've killed {self.player.enemies_killed} enemies and travelled {self.player.distance_travelled} mile(s).")
        exit()

    def generate_loot(self):
        loot_pool = ["Quest Item", "Gold", "Zinder"]
        return random.choice(loot_pool)

    def handle_loot(self, loot):
        if loot == "Gold":
            gold_amount = random.randint(1, 100)
            self.player.stats["gold"] += gold_amount
            print(f"You found {gold_amount} gold!")

        elif loot == "Quest Item":
            self.player.add_to_inventory("Quest Item") 
            print(f"You found {loot}!")

            for item, quantity in self.player.inventory.items():
                if item == "Quest Item" and quantity >= 4:
                    WorldStates.notify_boss_fight_requirement(self.player)
                    print("You've collected all the necessary quest items!")
                    

        elif loot == "Zinder":  
            self.player.zinders_collected += 1
            print(f"You found {loot}! You now have {self.player.zinders_collected} Zinders.")

        else:
            self.player.add_to_inventory(loot)
            print(f"You found {loot}!")