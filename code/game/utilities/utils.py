import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_dashes(x):
    dash = '-'
    border = dash * x
    print(border)

def print_status(player, enemy=None):
    print(f"{player.name} - HP: {'█' * int(player.health / 5)} ({player.health}/{player.MAX_HEALTH})\n".rjust(72))
    if enemy:
        print(f"{enemy.name} - HP: {'█' * int(enemy.health / 5)} ({enemy.health}/100)\n".rjust(72))

def fast_travel(player):
    print("You have arrived at the city.")
    while True:
        print_city_menu()
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
        elif choice == "t":
            stay_at_tavern(player)
        elif choice == "l":
            print("You leave the city.")
            break
        else:
            print("Invalid choice. Please try again.")

def stay_at_tavern(player):
    print("You decide to stay at the tavern for a rest.")
    player.health = player.MAX_HEALTH
    print("Your health has been fully restored.")

def buy_items(player):
    store_items = {
        "health potion": 20,
    }
    print("\nWelcome to the store!")
    print("Here are the items available for purchase:")
    for item, price in store_items.items():
        print(f"{item.capitalize()} - {price} gold")
    while True:
        print("Your Gold:", player.stats["gold"])
        choice = input("Enter the item you want to buy (or [done] to exit): ").lower()
        if choice == "done":
            break
        elif choice in store_items:
            if player.stats["gold"] >= store_items[choice]:
                player.add_to_inventory(choice)
                player.stats["gold"] -= store_items[choice]
                print(f"You bought {choice}!")
            else:
                print("You don't have enough gold to buy that.")
        else:
            print("That item is not available in the store.")

def print_city_menu():
        print("\nWelcome to the city!")
        print("What would you like to do?")
        print("[b]uy items")
        print("[c]heck inventory")
        print("[u]se item from inventory")
        print("[s]how character stats")
        print("[t]ravel to tavern")
        print("[l]eave city")

def print_welcome_messages(player_name):
    print(f"Welcome, {player_name}!")
    input("Press Enter to continue...")
    print("In this world of Lordran_Z, you must collect the four Quest Items.")
    input("Press Enter to continue...")
    print("Once you do, you will be summoned to fight the Dark Soulz Himself! haHA!")
    input("Press Enter to continue...")