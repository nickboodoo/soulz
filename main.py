from tests import TestCode
from tests import GamePlayLoop

def main():
    # initialization (if any)
    print("Initializing application...")

    # call functions or classes from other modules
    TestCode()
    # GamePlayLoop() - game appears to break (infinite loop) when the player goes out of bounds

if __name__ == "__main__":
    main()


