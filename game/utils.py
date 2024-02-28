import random
from .enemy import Enemy  # Importing the Enemy class from the enemy module

def print_status(player, enemy=None):
    print(f"{player.name} - HP: {'█' * int(player.stats['health'] / 5)} ({player.stats['health']}/{player.MAX_HEALTH})\n")
    if enemy:
        print(f"{enemy.name} - HP: {'█' * int(enemy.health / 5)} ({enemy.health}/100)\n")

def encounter_enemy(player):
    enemies = [
        Enemy("Goblin", 50, 10),
        Enemy("Skeleton", 40, 15),
        Enemy("Orc", 60, 12)
    ]
    enemy = random.choice(enemies)
    print(f"You've encountered a {enemy.name}!")
    player.encounters.append(enemy.name)

    while player.is_alive() and enemy.is_alive():
        print_status(player, enemy)
        choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

        if choice == "a":
            player_damage = player.attack()
            enemy.defend(player_damage)
            print(f"{player.name} attacks the {enemy.name} for {player_damage} damage.")
            if enemy.is_alive():
                enemy_damage = enemy.attack()
                player.defend(enemy_damage)
                print(f"The {enemy.name} attacks back for {enemy_damage} damage.")
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
        print(f"You defeated the {enemy.name}!")
        player.enemies_killed += 1
        # Chance to drop a quest item
        if len(player.quest_items_collected) < 4:  # Check if all quest items are not collected
            drop_rate = 0.2 / (4 - len(player.quest_items_collected))  # Adjust drop rate based on remaining quest items
            if random.random() < drop_rate:
                available_items = list(set(["Quest Item 1", "Quest Item 2", "Quest Item 3", "Quest Item 4"]) - player.quest_items_collected)
                quest_item = random.choice(available_items)
                print(f"The {enemy.name} dropped {quest_item}!")
                player.quest_items_collected.add(quest_item)
                print(f"You've collected {len(player.quest_items_collected)} out of 4 quest items.")
            else:
                print("No quest item dropped this time.")
        else:
            print("All quest items collected!")
    else:
        print("You lost the battle!")
        print(f"You've killed {player.enemies_killed} enemies and travelled {player.distance_travelled} miles.")
        exit()

def travel_to_city(player):
    print("You have arrived at the city.")
    while True:
        print("\nWelcome to the city!")
        print("What would you like to do?")
        print("[b]uy items")
        print("[c]heck inventory")
        print("[u]se item from inventory")
        print("[s]how character stats")
        print("[l]eave city")
        choice = input("Enter your choice: ").lower()
        if choice == "b":
            buy_items(player)
        elif choice == "c":
            player.check_inventory()
        elif choice == "u":
            item_to_use = input("Enter the item you want to use from your inventory: ").lower()
            player.use_item(item_to_use)
        elif choice == "s":
            player.view_character_stats()
        elif choice == "l":
            print("You leave the city.")
            break
        else:
            print("Invalid choice. Please try again.")
