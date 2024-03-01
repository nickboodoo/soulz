# Helper function to show HP bars
def print_status(player, enemy=None):
    print(f"{player.name} - HP: {'█' * int(player.stats['health'] / 5)} ({player.stats['health']}/{player.MAX_HEALTH})\n")

    # Shows enemy health bar ONLY if enemy is present since enemy=None
    if enemy:
        print(f"{enemy.name} - HP: {'█' * int(enemy.health / 5)} ({enemy.health}/100)\n")

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
    player.stats["health"] = player.MAX_HEALTH  # Fully replenish player's health
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
