import random
from game.utilities.utils import clear_screen, fast_travel
from game.sequence_loops.battle_manager import BattleManager
from game.characters.enemy import Enemy
from game.utilities.boss_battle import BossBattle

class GameLoop:
    def __init__(self, player, world_state):
        self.player = player
        self.world_state = world_state
        self.locations = {
            'start': {'description': 'You are at the starting point of your adventure.', 'neighbors': ['forest', 'river'], 'visited': False},
            'forest': {'description': 'A dense forest, full of unknown creatures.', 'neighbors': ['start', 'cave'], 'visited': False},
            'river': {'description': 'A calm river. You can hear something in the distance.', 'neighbors': ['start'], 'visited': False},
            'cave': {'description': 'A dark cave. It feels like something powerful is nearby.', 'neighbors': ['forest'], 'boss': True, 'visited': False}
        }
        self.current_location = 'start'
        self.cleared_locations = set()

    def start_loop(self):
        while self.player.is_alive():
            choice = input("\nWhat would you like to do? [explore], [fast travel], or [quit]? ").lower()
            clear_screen()

            if choice == "explore":
                self.explore()
            elif choice == "fast travel":
                fast_travel(self.player)
            elif choice == "quit":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please try again.")

        if not self.player.is_alive():
            print("Game over.")

    def explore(self):
        location = self.locations[self.current_location]
        print(location['description'])
        
        if location['visited']:
            print("You have already been here.")
            if self.current_location in self.cleared_locations:
                print("This location has been cleared. There's nothing more to find here.")
        
        if 'boss' in location and not location['visited']:
            final_boss_battle = BossBattle(self.player)
            final_boss_battle.battle_soul_of_zinder()
            location['visited'] = True
        
        self.show_neighbors_and_move()

    def show_neighbors_and_move(self):
        neighbors = self.locations[self.current_location]['neighbors']
        print("\nYou can travel to:")
        for i, neighbor in enumerate(neighbors, start=1):
            print(f"{i}. {neighbor}")
        print(f"{len(neighbors)+1}. Fast travel to the city")
        
        choice = input("Where would you like to go? Enter number: ")
        try:
            if int(choice) == len(neighbors) + 1:
                fast_travel(self.player)
            else:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(neighbors):
                    self.current_location = neighbors[choice_index]
                    self.locations[self.current_location]['visited'] = True
                    self.handle_location_events()
                else:
                    print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")

    def handle_location_events(self):
        if self.current_location in self.cleared_locations:
            print(f"You return to {self.current_location}, but it remains quiet.")
        else:
            encounter_chance = random.randint(1, 10)
            if encounter_chance <= 7:
                enemy_battle = BattleManager(self.player)
                enemy = Enemy.create_random_enemy()
                enemy_battle.start_battle(enemy)
                self.cleared_locations.add(self.current_location)
            else:
                print(f"While exploring {self.current_location}, you found nothing of interest.")
                self.cleared_locations.add(self.current_location)
        # After handling location events, always allow the player to decide their next move.
        self.show_neighbors_and_move()
