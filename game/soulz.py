from managers.game_setup import GameSetup


if __name__ == "__main__":

    input("Welcome to Soulz!")

    setup = GameSetup()
    setup.initialize_game_settings("A", "D")
    setup.setup_game()
    setup.initiate_gameplay_loop()

    
