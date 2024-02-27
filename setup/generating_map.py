import random

class GeneratingMap:
    # Define dimensions of the map
    MAP_WIDTH = 10
    MAP_HEIGHT = 10

    @staticmethod
    # Function to generate a random map
    def generate_map(width, height):
        # Initialize an empty map
        new_map = [[' ' for _ in range(width)] for _ in range(height)]

        # Add some random obstacles or features
        for i in range(height):
            for j in range(width):
                # 10% chance of an obstacle in a cell
                if random.random() < 0.1:
                    new_map[i][j] = '#'
                # 5% chance of a special feature in a cell
                elif random.random() < 0.05:
                    new_map[i][j] = '*'

        return new_map

    @staticmethod
    # Function to print the map with borders
    def print_map_with_border(game_map):
        print('+' + '-' * (GeneratingMap.MAP_WIDTH * 2 - 1) + '+')
        for row in game_map:
            print('|' + ' '.join(row) + '|')
        print('+' + '-' * (GeneratingMap.MAP_WIDTH * 2 - 1) + '+')

# Generate a random map
game_map = GeneratingMap.generate_map(GeneratingMap.MAP_WIDTH, GeneratingMap.MAP_HEIGHT)

# Print the map with borders
GeneratingMap.print_map_with_border(game_map)
