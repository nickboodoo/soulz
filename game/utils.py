import os

# CLEARS SCREEN

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# PRINTS DASHES

def print_dashes(x):
    dash = '-'
    border = dash * x
    print(border)
        

