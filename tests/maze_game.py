class GamePlayLoop:
    def __init__(self):

        # Map layout represented as a 2D array of 16 rooms
        # There are 6 Rooms with Golden Spoons and 1 Room with the Angry Chef.
        list_rooms = [
            [[1, "Empty", "Front Door"], [2, "Empty", "Atrium"], [3, "Golden Spoon", "Closet"], [4, "Empty", "Bedroom"]],
            [[5, "Empty", "Bathroom"], [6, "Golden Spoons", "Living Room"], [7, "Empty", "Grand Hallway"],
            [8, "Golden Spoons", "Family Room"]],
            [[9, "Empty", "Indoor Garden"], [10, "Angry Chef", "Kitchen"], [11, "Empty", "Laundry Room"], [12, "Empty", "Master Bedroom"]],
            [[13, "Golden Spoons", "Master Bathroom"], [14, "Golden Spoons", "Guest Bedroom"], [15, "Empty", "Movie Theater"],
            [16, "Golden Spoons", "Spa"]]
        ]

        total_items_collected = 0  # Player's inventory.
        room_x, room_y = 0, 0  # Coordinates representing player location.


        print("Dinner Party Maze Game")
        print("by Nick Boodoo")
        input()
        print()
        print("In this game, you will be playing as the assistant to a very angry chef.")
        print("His reputation is on the line because he is throwing a dinner party for a very respected guest,")
        print("however he seems to have misplaced his Golden Spoons.")
        print("If you can't find his 6 Golden Spoons that are scattered throughout the mansion, you are fired!!")
        print("Press ENTER if you wish to start the game")
        input()



                


        # Gameplay loop
        while True:
            current_room = list_rooms[room_x][room_y][0]  # Retrieve planet location from array.
            room_content = list_rooms[room_x][room_y][1]  # Retrieve planet content from array.
            room_name = list_rooms[room_x][room_y][2]  # Retrieves planet name from array.

            """
            The player wins the game by retrieving all 6 Golden Spoons before
            encountering the room with the Angry Chef. The player loses the game by
            moving to the room with the Angry Chef before collecting all 6 Golden Spoons.
            """

            if room_content == "Angry Chef":
                if total_items_collected < 6:
                    print("\nYou encounter Angry Chef. Sadly you do not have enough Golden Spoons so you were kicked"
                        "out of the party.")
                    print(input('Thanks for playing. Press ENTER to Exit'))
                    break
                else:
                    print("\nYou saved the dinner party\nCongrats!")
                    print(input('Thanks for playing. Press ENTER to Exit'))
                    break

            # Room navigation loop.
            while True:
                print('-----------------------------------------------------')
                print("\nYou are in the ", room_name)  # Shows the player's current location.
                print('You have', total_items_collected, "Golden Spoons\n")  # Shows the player's current inventory.
                if room_content == "Empty":
                    print(room_name, "is empty! Nothing can be collected\n")
                    print("Enter the direction you'd like to travel:\n1.North 2.South 3.East 4.West")

                    # Modifying player position. For each direction, make sure player stays in bounds.
                    try:
                        option = int(input())  # Takes player input for direction.
                        # Move the player North.
                        if option == 1 and room_x - 1 >= 0:
                            room_x -= 1
                            break
                        # Move the player South.
                        elif option == 2 and room_x + 1 <= 3:
                            room_x += 1
                            break
                        # Move the player East.
                        elif option == 3 and room_y + 1 <= 3:
                            room_y += 1
                            break
                        # Move the player West.
                        elif option == 4 and room_y - 1 >= 0:
                            room_y -= 1
                            break
                        # Describe bounds from which the player cannot deviate.
                        else:
                            print("\nSorry, you don't have the key for that room.")
                        break
                    except ValueError:  # Non-integer player input will be redirected here.
                        print("Oops! Try again and enter a number this time!")

                # For a room with Golden Spoon
                elif room_content == "Golden Spoon":
                    print('You see a Golden Spoon')
                    print("Enter one of the following:\nY.Pick Up Item N. Leave Item\n")
                    option = str(input()).upper()
                    # Take player input to add Golden Spoon to inventory.
                    if option == 'Y':  # Take player input to add Golden Spoon to inventory.
                        # Set room to empty if the player added the Golden Spoon to their inventory.
                        list_rooms[room_x][room_y][1] = "Empty"
                        print("You collected a Golden Spoon")
                        # Increment Golden Spoons
                        total_items_collected += 1
                        break
                    elif option == 'N':  # Take player input to leave Golden Spoon.
                        print('Are you sure? You cannot continue without it.')
                        break