import os

# CLEARS SCREEN

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# PRINTS DASHES

def print_dashes(x):
    dash = '-'
    border = dash * x
    print(border)

# PRINTS HP BARS

def print_status(player, enemy=None):
    print(f"{player.name} - HP: {'█' * int(player.health / 5)} ({player.health}/{player.MAX_HEALTH})\n".rjust(72))
    if enemy:
        print(f"{enemy.name} - HP: {'█' * int(enemy.health / 5)} ({enemy.health}/100)\n".rjust(72))

# PRINT PLAYER MENU

def navigate_player_menu(player):
    while True:
        print_player_menu()
        choice = input("Enter your choice: ").lower()
        clear_screen()
        if choice == "b":
            buy_items(player)
        elif choice == "c":
            player.check_inventory()
        elif choice == "u":
            player.check_inventory()
            item_to_use = input("Enter the item you want to use from your inventory: ").lower()
            clear_screen()
            player.use_item(item_to_use)
        elif choice == "s":
            player.view_character_stats()
        elif choice == "t":
            stay_at_tavern(player)
        elif choice == "l":
            input("You leave the city.")
            clear_screen()
            break
        else:
            print("Invalid choice. Please try again.")

# CALL THIS FUNCTION TO FULL HEAL PLAYER (FROM PLAYER MENU)

def stay_at_tavern(player):
    print("You decide to stay at the tavern for a rest.")
    player.health = player.MAX_HEALTH
    input("Your health has been fully restored.")
    clear_screen()

# CALL THIS FUNCTION TO SELL ITEMS TO PLAYER (FROM PLAYER MENU)

def buy_items(player):
    store_items = {
        "health potion": 20,  # Cost per item
    }
    print("\nWelcome to the store!")
    print("Here are the items available for purchase:")

    while True:
        print("\nYour Gold:", player.stats["gold"])
        for item, price in store_items.items():
            print(f"{item.capitalize()} - {price} gold each")

        item_choice = input("\nEnter the item you want to buy (or [done] to exit): ").lower()
        clear_screen()

        if item_choice == "done":
            break

        elif item_choice in store_items:
            try:
                quantity = int(input(f"How many {item_choice}s would you like to buy? "))
                if quantity <= 0:
                    raise ValueError  # Handle non-positive integers
            except ValueError:
                print("Please enter a valid number.")
                input("Press Enter to continue...")
                clear_screen()
                continue

            total_cost = store_items[item_choice] * quantity
            if player.stats["gold"] >= total_cost:
                player.add_to_inventory(item_choice, quantity)
                player.stats["gold"] -= total_cost
                print(f"You bought {quantity} {item_choice}(s) for {total_cost} gold!")
                input("Press Enter to continue...")
                clear_screen()
            else:
                print("You don't have enough gold for that purchase.")
                input("Press Enter to continue...")
                clear_screen()
        else:
            print("That item is not available in the store.")
            input("Press Enter to continue...")
            clear_screen()


# PRINT PLAYER MENU

def print_player_menu():
        print("\nPLAYER MENU")
        print("What would you like to do?")
        print("[b]uy items")
        print("[c]heck inventory")
        print("[u]se item from inventory")
        print("[s]how character stats")
        print("[t]ravel to tavern")
        print("[l]eave city")

# CALCULATES SHORTEST PATH (GOAL)

def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge_info in graph.edges[min_node]:
            edge, _ = edge_info
            weight = current_weight + graph.difficulties[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path