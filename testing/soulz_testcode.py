import random
import os

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.strength = attack

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        damage = self.strength
        target.health -= damage
        return damage

class Player:
    def __init__(self, name='Player', health=100, attack=10):
        self.name = name
        self.health = health
        self.strength = attack

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        damage = self.strength
        target.health -= damage
        return damage

    def heal(self):
        heal_amount = 20
        self.health += heal_amount
        return heal_amount

class Location:
    def __init__(self, name, generate_enemy_flag=True):
        self.name = name
        self.connections = []
        self.visited = False
        self.enemy = self.generate_enemy() if generate_enemy_flag else None

    def connect(self, node):
        if node not in self.connections:
            self.connections.append(node)
            node.connections.append(self)

    def generate_enemy(self):
        if random.choice([True, False]):
            return Enemy("Goblin", health=25, attack=random.randint(1, 5))
        return None

class Map:
    def __init__(self, size):
        self.nodes = [Location("Room 0", generate_enemy_flag=False)] + [Location(f"Room {i}") for i in range(1, size)]
        self.generate_graph()

    def generate_graph(self):
        for i in range(len(self.nodes) - 1):
            self.nodes[i].connect(self.nodes[i + 1])
            if i > 0 and random.choice([True, False]):
                self.nodes[i].connect(random.choice(self.nodes[:i]))

class GameScreen:
    def __init__(self, location):
        self.location = location

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_dashes(self, x=30):
        print('-' * x)

    def display(self):
        pass

class VictoryScreen(GameScreen):
    def display(self):
        self.clear_screen()
        print("Congratulations! You have defeated all the enemies and survived.")
        print("You are a true hero!")
        print("\nWould you like to play again? (yes/no)")
        choice = input().lower()
        if choice == 'yes':
            game = GameLoop()
            game.play()
        else:
            print("Thank you for playing! Goodbye.")
            exit()

class DefeatScreen(GameScreen):
    def display(self):
        self.clear_screen()
        print("Alas, you have been defeated. The world mourns the loss of a brave hero.")
        print("\nWould you like to try again? (yes/no)")
        choice = input().lower()
        if choice == 'yes':
            game = GameLoop()
            game.play()
        else:
            print("Thank you for playing! Better luck next time.")
            exit()

class ExplorationScreen(GameScreen):
    def __init__(self, location, game_loop):
        super().__init__(location)
        self.game_loop = game_loop

    def display(self):
        while True:
            self.clear_screen()
            print(f"You are in {self.location.name}.")
            if self.location.enemy and self.location.enemy.is_alive():
                print(f"An enemy {self.location.enemy.name} is here!")
            print("Connections:")
            for i, connection in enumerate(self.location.connections):
                print(f" {i + 1}: {connection.name}")
            print("\nChoose an action: \n l: List rooms \n [number]: Move to connection \n q: Quit")
            
            action = input("What do you want to do? ")
            self.clear_screen()

            if action == 'l':
                self.display_rooms(self.game_loop.graph.nodes)
            elif action.isdigit() and int(action) - 1 < len(self.location.connections):
                self.game_loop.current_node = self.location.connections[int(action) - 1]
                self.game_loop.current_node.visited = True
                break
            elif action == 'q':
                exit()
            else:
                print("Invalid action, try again.")
                input("Press Enter to continue...")
                self.clear_screen()

    def display_rooms(self, nodes):
        print("Rooms:")
        for node in nodes:
            visited_marker = "Visited" if node.visited else "Not Visited"
            print(f"{node.name}: {visited_marker}")
        input("Press Enter to continue...")
        self.clear_screen()

class CombatScreen(GameScreen):
    def __init__(self, location, player, enemy):
        super().__init__(location)
        self.player = player
        self.enemy = enemy

    def display_combat_options(self):
        print("Choose your action: \n1. Attack \n2. Use Item \n3. Flee")

    def handle_combat_action(self):
        action = input("Action: ")
        self.clear_screen()

        if action == "1":
            damage_dealt = self.player.attack(self.enemy)
            print(f"You attack the {self.enemy.name} for {damage_dealt} damage.")
            if not self.enemy.is_alive():
                print(f"The {self.enemy.name} is defeated.")
                return 'enemy_defeated'
            damage_taken = self.enemy.attack(self.player)
            print(f"The {self.enemy.name} attacks you for {damage_taken} damage.")
        elif action == "2":
            heal_amount = self.player.heal()
            print(f"You heal for {heal_amount} health.")
        elif action == "3":
            print("You flee back to the previous location.")
            return 'fled'
        else:
            print("Invalid action, try again.")
        return 'continue'

    def display(self):
        print(f"You encounter an enemy! The fight begins. It's a {self.enemy.name}.")
        while self.player.is_alive() and self.enemy.is_alive():
            self.display_combat_options()
            result = self.handle_combat_action()
            if result in ['enemy_defeated', 'fled']:
                break
            if not self.player.is_alive():
                print("Game Over. You have been defeated.")
                break

class GameLoop:
    def __init__(self, size=3):
        self.graph = Map(size)
        self.current_node = self.graph.nodes[0]
        self.player = Player()

    def update_screen(self):
        if not self.player.is_alive():
            # Transition to DefeatScreen if player is defeated
            self.current_screen = DefeatScreen(self.current_node)
        elif self.have_defeated_all_enemies():
            # Transition to VictoryScreen if all enemies are defeated
            self.current_screen = VictoryScreen(self.current_node)
        elif self.current_node.enemy and self.current_node.enemy.is_alive():
            self.current_screen = CombatScreen(self.current_node, self.player, self.current_node.enemy)
        else:
            self.current_screen = ExplorationScreen(self.current_node, self)

    def play(self):
        while self.player.is_alive() and not self.have_defeated_all_enemies():
            self.update_screen()
            self.current_screen.display()

        # Handle game end state outside the loop
        if not self.player.is_alive():
            DefeatScreen(self.current_node).display()
        elif self.have_defeated_all_enemies():
            VictoryScreen(self.current_node).display()


    def have_defeated_all_enemies(self):
        return all(not node.enemy or not node.enemy.is_alive() for node in self.graph.nodes)

if __name__ == "__main__":
    game = GameLoop()
    game.play()

