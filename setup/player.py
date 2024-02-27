from .generating_map import GeneratingMap

class Game:
    def __init__(self):
        self.player = Player(0, 0)
        self.game_map = GeneratingMap.generate_map(GeneratingMap.MAP_WIDTH, GeneratingMap.MAP_HEIGHT)
        self.game_map[self.player.y][self.player.x] = 'P'

    def print_map(self):
        border = '+' + '-' * (len(self.game_map[0]) + 2) + '+'
        print(border)
        for row in self.game_map:
            print('|' + ''.join(row) + '|')
        print(border)

    def clear_screen(self):
        # Code to clear the screen
        pass

    def move_player(self, dx, dy):
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        if 0 <= new_x < GeneratingMap.MAP_WIDTH and 0 <= new_y < GeneratingMap.MAP_HEIGHT:
            self.game_map[self.player.y][self.player.x] = ' '  # Clear old position
            self.player.x = new_x
            self.player.y = new_y
            self.game_map[self.player.y][self.player.x] = 'P'  # Update new position

    def run(self):
        while True:
            self.clear_screen()
            self.print_map()
            direction = input("Enter direction to move (w/a/s/d): ").lower()
            if direction == 'w':
                self.move_player(0, -1)
            elif direction == 'a':
                self.move_player(-1, 0)
            elif direction == 's':
                self.move_player(0, 1)
            elif direction == 'd':
                self.move_player(1, 0)
            else:
                print("Invalid input!")
                continue

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Initialize and run the game
game = Game()
game.run()
