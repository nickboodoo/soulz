class Debuff:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def apply(self, target):
        print(f"Applying {self.name} to {target} for {self.duration} seconds.")



if __name__ == "__main__":
    print("This is a testing file.")

    enemy = "Goblin"
    Debuff("Poison", 5).apply(enemy)
