import random
from .enemy import Enemy  # Importing the Enemy class from the enemy module
from .player import Player

# Helper function to show HP bars
def print_status(player, enemy=None):
    print(f"{player.name} - HP: {'█' * int(player.stats['health'] / 5)} ({player.stats['health']}/{player.MAX_HEALTH})\n")

    # Shows enemy health bar ONLY if enemy is present since enemy=None
    if enemy:
        print(f"{enemy.name} - HP: {'█' * int(enemy.health / 5)} ({enemy.health}/100)\n")

# Helper funtion to simulate an encounter between the player and a randomly chosen enemy
def encounter_enemy(player):
    # Create enemies
    enemies = [
        Enemy("Goblin", 50, 10),
        Enemy("Skeleton", 40, 15),
        Enemy("Orc", 60, 12)
    ]

    # Select random enemy
    enemy = random.choice(enemies)

    # Display encounter message to player
    print(f"You've encountered a {enemy.name}!")

    # Store all of player's enemy encounter
    # Data structure does not exist, game will break if player access this variable
    player.encounters.append(enemy.name)

    # Combat loop
    while player.is_alive() and enemy.is_alive():
        print_status(player, enemy)
        choice = input("Choose your action: [a]ttack, [u]se item, [f]lee: ").lower()

        # Attack logic
        if choice == "a":
            player_damage = player.attack()
            enemy.defend(player_damage)
            print(f"{player.name} attacks the {enemy.name} for {player_damage} damage.")

            if enemy.is_alive():
                enemy_damage = enemy.attack()
                player.defend(enemy_damage)
                print(f"The {enemy.name} attacks back for {enemy_damage} damage.")
        
        # Use Item logic
        elif choice == "u":
            player.check_inventory()
            item_to_use = input("Enter the item you want to use (or [cancel] to go back): ").lower()

            if item_to_use == "cancel":
                continue

            player.use_item(item_to_use)

        # Flee logic
        elif choice == "f":
            print("You fled from the battle!")
            return
        
        # Input error handling
        else:
            print("Invalid choice. Please try again.")

    # Battle outcome
    if player.is_alive():
        print(f"You defeated the {enemy.name}!")
        player.enemies_killed += 1

        # Player level-up logic
        if player.enemies_killed % 3 == 0:  # Check if the player has defeated a multiple of 3 enemies
            player.level_up()  # Level up the player every 3rd enemy defeated

        # Available loot for rewards
        loot_pool = ["Quest Item", "Health Potion", "Gold", "Zinder"]
        loot = random.choice(loot_pool)

        if loot == "Gold":
            gold_amount = random.randint(1, 100)
            player.stats["gold"] += gold_amount
            print(f"You found {gold_amount} gold!")

        elif loot == "Quest Item":
            player.add_to_inventory("Quest Item") 
            print(f"You found {loot}!")

            for item, quantity in player.inventory.items():
                if item == "Quest Item":
                    if quantity >= 4:
                        print("You've collected all the necessary quest items!")
                        battle_soul_of_zinder(player)  # Trigger boss fight with Soul of Zinder

        elif loot == "Zinder":  
            player.zinders_collected += 1 # If Zinder is found, increase the Zinders collected
            print(f"You found {loot}! You now have {player.zinders_collected} Zinders.")

        else:
            player.add_to_inventory(loot)
            print(f"You found {loot}!")

    # Player loses the game
    else:
        print("You lost the battle!")
        print(f"You've killed {player.enemies_killed} enemies and travelled {player.distance_travelled} mile(s).")
        exit()

# Helper function for one of the player's main menus
def fast_travel(player):
    print("You have arrived at the city.")

    # Display the City Activities menu to the player
    while True:
        print("\nWelcome to the city!")
        print("What would you like to do?")
        print("[b]uy items")
        print("[c]heck inventory")
        print("[u]se item from inventory")
        print("[s]how character stats")
        print("[t]ravel to tavern")
        print("[l]eave city")
        choice = input("Enter your choice: ").lower()

        if choice == "b":

            # Call Helper-helper function
            buy_items(player)

        elif choice == "c":
            player.check_inventory()
            
        elif choice == "u":
            item_to_use = input("Enter the item you want to use from your inventory: ").lower()
            player.use_item(item_to_use)

        elif choice == "s":
            player.view_character_stats()

        elif choice == "t":

            # Call Helper-helper function
            stay_at_tavern(player)

        elif choice == "l":
            print("You leave the city.")
            break

        # Error handling
        else:
            print("Invalid choice. Please try again.")

# Helper-helper function for enabling the player to full heal at a tavern
def stay_at_tavern(player):
    print("You decide to stay at the tavern for a rest.")
    player.stats["health"] = player.MAX_HEALTH  # Fully replenish player's health
    print("Your health has been fully restored.")

# Helper-helper function for enabling the player to buy items from the store
def buy_items(player):
    store_items = {
        "health potion": 20,
    }

    # Start of store menu
    print("\nWelcome to the store!")
    print("Here are the items available for purchase:")

    for item, price in store_items.items():
        print(f"{item.capitalize()} - {price} gold")

    while True:
        print("Your Gold:", player.stats["gold"])
        choice = input("Enter the item you want to buy (or [done] to exit): ").lower()

        # Go back to previous menu (Store menu)
        if choice == "done":
            break

        # Check if player can buy item
        elif choice in store_items:
            if player.stats["gold"] >= store_items[choice]:
                player.add_to_inventory(choice)
                player.stats["gold"] -= store_items[choice]
                print(f"You bought {choice}!")

            else:
                print("You don't have enough gold to buy that.")

        # Input error handling
        else:
            print("That item is not available in the store.")

def battle_soul_of_zinder(player):
    soul_of_zinder = Enemy("Soul of Zinder", 200, 20)
    print(f"A fearsome enemy, the {soul_of_zinder.name}, blocks your path!")
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
        # Rewards for defeating the final boss can be added here
        quit()

    else:
        print("You lost the battle against the Soul of Zinder!")
