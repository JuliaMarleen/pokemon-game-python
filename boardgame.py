import os
import random
import json
import time

questions = open('boardgame_questions.json')
data = json.load(questions)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


places = [24, 26, 28, 30, 32, 34, 36,
          38, 40, 42, 64, 86, 108, 130, 152,
          174, 196, 194, 192, 190, 188, 186,
          184, 182, 180, 178, 156, 134, 112,
          90, 68, 46, 24]

player1 = {
    "name": f"{bcolors.OKCYAN}Player 1{bcolors.ENDC}",
    "collected_pokemon": [],
    "money": 0,
    "location": 0,
    "place_on_board": 0
}
player2 = {
    "name": f"{bcolors.WARNING}Player 2{bcolors.ENDC}",
    "collected_pokemon": [],
    "money": 0,
    "location": 0,
    "place_on_board": 0
}

items = [
    {
        "name": f"{bcolors.OKGREEN}Bulbasaur{bcolors.ENDC}",
        "id": 1,
        "points": 3,
        "starter": True
    },
    {
        "name": f"{bcolors.FAIL}Charmander{bcolors.ENDC}",
        "id": 2,
        "points": 1,
        "starter": True
    },
    {
        "name": f"{bcolors.OKCYAN}Squirtle{bcolors.ENDC}",
        "id": 3,
        "points": 2,
        "starter": True
    },
    {
        "name": f"{bcolors.WARNING}Pikachu{bcolors.ENDC}",
        "id": 4,
        "points": 2,
        "starter": False
    },
    {
        "name": f"{bcolors.OKBLUE}Magikarp{bcolors.ENDC}",
        "id": 5,
        "points": 3,
        "starter": False
    },
    {
        "name": f"{bcolors.HEADER}Eevee{bcolors.ENDC}",
        "id": 6,
        "points": 4,
        "starter": False
    },
    {
        "name": f"{bcolors.WARNING}Psyduck{bcolors.ENDC}",
        "id": 7,
        "points": 1,
        "starter": False
    },
    {
        "name": f"{bcolors.BOLD}Onix{bcolors.ENDC}",
        "id": 8,
        "points": 2,
        "starter": False
    }
]

gamename = """
____            _  _
|    \   ___   | |/ /   _/_   __  __   ___    __  _
|   _/  / _ \  |   |   /  _\ |  \/  | / _ \  |  \| |
|__|    \___/  |_|\_\  \__\  |_|\/|_| \___/  |_|\__|
"""

board = """
_____________________
|>|*|_|?|_|$|_|?|_| |
| |               |?|
|$|               | |
| |               |*|
|*|               | |
| |               |?|
|?|_______________| |
|_|?|_|$|_|*|_|?|_|$|
"""


def print_board():
    playboard = 0
    if (player2["place_on_board"] == 0):
        playboard = board[:player1["place_on_board"]] + \
            f'{bcolors.OKCYAN}{bcolors.UNDERLINE}1{bcolors.ENDC}{bcolors.OKGREEN}' + \
            board[player1["place_on_board"] + 1:]

    elif (player1["place_on_board"] <= player2["place_on_board"]):
        playboard = board[:player1["place_on_board"]] + f'{bcolors.OKCYAN}{bcolors.UNDERLINE}1{bcolors.ENDC}{bcolors.OKGREEN}' + board[player1["place_on_board"] +
                                                                                                                                       1:player2["place_on_board"]] + f'{bcolors.WARNING}{bcolors.UNDERLINE}2{bcolors.ENDC}{bcolors.OKGREEN}' + board[player2["place_on_board"] + 1:]

    elif (player2["place_on_board"] <= player1["place_on_board"]):
        playboard = board[:player2["place_on_board"]] + f'{bcolors.WARNING}{bcolors.UNDERLINE}2{bcolors.ENDC}{bcolors.OKGREEN}' + board[player2["place_on_board"] +
                                                                                                                                        1:player1["place_on_board"]] + f'{bcolors.OKCYAN}{bcolors.UNDERLINE}1{bcolors.ENDC}{bcolors.OKGREEN}' + board[player1["place_on_board"] + 1:]
    os.system('cls' if os.name == 'nt' else 'clear')
    stats()
    print(f"{bcolors.OKGREEN}{str(playboard)}{bcolors.ENDC}")

# Printing current points and pokemon.


def stats():
    print(f"{bcolors.WARNING}{gamename}{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}Collect all 8 Pokemon!!{bcolors.ENDC} \n")
    print(player1["name"],
          f"{bcolors.OKCYAN}points:{bcolors.ENDC}", player1["money"])
    print(player1["name"], f"{bcolors.OKCYAN}pokemon:{bcolors.ENDC}", end=" ")
    for pokemon in player1["collected_pokemon"]:
        print(pokemon["name"], end=" ")
    print("\n")

    print(player2["name"],
          f"{bcolors.WARNING}points:{bcolors.ENDC}", player2["money"])
    print(player2["name"], f"{bcolors.WARNING}pokemon:{bcolors.ENDC}", end=" ")
    for pokemon in player2["collected_pokemon"]:
        print(pokemon["name"], end=" ")
    print("\n")


# When at the end of the circle of the board, reset position to make a new loop


def loop_board(player):
    if (player["location"] >= len(places)):
        player["location"] = player["location"] - len(places)

# Detecting on what kind of square they are


def special_square(player):
    if board[player["place_on_board"]] == '$':
        store(player)

    elif board[player["place_on_board"]] == '*':
        extra_item(player)

    elif board[player["place_on_board"]] == '?':
        quiz(player)
    else:
        print("Nothing special......")


def store(player):
    print('Welcome in the Pokestore!')
    print(f"{bcolors.OKCYAN}{bcolors.BOLD}current points: {bcolors.ENDC}",
          f"{bcolors.OKCYAN}{bcolors.BOLD}{player['money']}{bcolors.ENDC}")
    print('What Pokemon do you want to have? \n')
    for item in items:
        tab = "\t"
        if len(str(item["name"])) <= 13:
            tab = "\t \t"
        print(item["id"], item["name"], tab + str(item["points"]) + "points")
    buy = input('Type number or none?')
    if buy != "none" and buy != '':
        buy = int(buy)
        for item in items:
            if item["id"] == buy:
                already_caught = False
                for pokemon in player["collected_pokemon"]:
                    if pokemon == item:
                        print(
                            f"{bcolors.BOLD}Too bad, you already have this pokemon!{bcolors.ENDC}")
                        already_caught = True

                if already_caught == False:
                    if item["points"] <= player["money"]:
                        player["collected_pokemon"].append(item)
                        player["money"] = player["money"] - item["points"]
                        print("You bought", item["name"], "!!")
                        check_won(player)
                    else:
                        print(
                            f"{bcolors.BOLD}You don't have enough points! Byebye!{bcolors.ENDC}")
    else:
        print(f"{bcolors.BOLD}Byebye!{bcolors.ENDC}")

# Receiving random pokemon


def extra_item(player):
    # print('Cadeautje!')
    rand_int = random.randint(0, len(items)-1)
    new_pokemon = items[rand_int]
    print("A wild", new_pokemon["name"], "appeared!")
    already_caught = False

    for pokemon in player["collected_pokemon"]:
        if pokemon == new_pokemon:
            print(
                f"{bcolors.BOLD}Too bad you already have this pokemon!{bcolors.ENDC}")
            already_caught = True

    if already_caught == False:
        player["collected_pokemon"].append(new_pokemon)
        print("You cought it!")
        check_won(player)

# Quizzz


def quiz(player):
    print(f"{bcolors.OKBLUE}You landed on a questionmark!{bcolors.ENDC}")
    rand_int = random.randint(0, len(data['questions'])-1)
    question = data['questions'][rand_int]
    print(f"{bcolors.BOLD}{question['question']}{bcolors.ENDC}")
    for answer_option in question['answers']:
        print(answer_option)
    given_answer = input(
        f"{bcolors.OKBLUE}(Type the letter:){bcolors.ENDC}").capitalize()
    if given_answer == question['correct']:
        print(
            f"{bcolors.OKCYAN}{bcolors.BOLD}That's the right answer! You earn 2 points{bcolors.ENDC}")
        player["money"] = player["money"] + 2
    else:
        print('Nope. No points for you')

# When receiving a new pokemon, check if someone has 8 pokemon already


def check_won(player):
    if len(player["collected_pokemon"]) == 8:
        os.system('cls' if os.name == 'nt' else 'clear')
        stats()
        print_board()
        print("YOU WON!", player["name"], "You cought all 8 pokemon!")
        if player == player1:
            print("Before your rival", player2["name"], "did!")
        else:
            print("Before your rival", player1["name"], "did!")
        print("Congratulations!!")
        input("\n\nThis is the end of the game, would you like to start again?")
        game_reset()
        start_of_game()


def game_reset():
    player1["name"] = f"{bcolors.OKCYAN}Player 1{bcolors.ENDC}"
    player1["collected_pokemon"] = []
    player1["money"] = 0
    player1["location"] = 0
    player1["place_on_board"] = 0

    player2["name"] = f"{bcolors.WARNING}Player 2{bcolors.ENDC}"
    player2["collected_pokemon"] = []
    player2["money"] = 0
    player2["location"] = 0
    player2["place_on_board"] = 0


# Explanation of the board


def explain():
    os.system('cls' if os.name == 'nt' else 'clear')
    stats()
    print(f"{bcolors.OKGREEN}{board}{bcolors.ENDC}")
    print("welcome", player1["name"], "and",
          player2["name"], "to this mystical pokemon world!\n")
    print(player1["name"], "What is your name?")
    name = input()
    player1["name"] = f"{bcolors.OKCYAN}{name}{bcolors.ENDC}"
    print()
    print(player2["name"], "What is your name?")
    name = input()
    player2["name"] = f"{bcolors.WARNING}{name}{bcolors.ENDC}"
    print()
    print("Hello", player1["name"], "and", player2["name"])

    input(f"{bcolors.BOLD}Let me first explain the board to you.{bcolors.ENDC}\n")
    print("There are a few special squares:")
    input(f"{bcolors.OKGREEN}{bcolors.BOLD}$ = the store, you can buy pokemon with points!{bcolors.ENDC}")
    input(f"{bcolors.OKBLUE}{bcolors.BOLD}? = the quiz, answer questions to earn points!{bcolors.ENDC}")
    input(f"{bcolors.OKCYAN}{bcolors.BOLD}* = random encounters with pokemon!{bcolors.ENDC}")
    input("Let's continue!")

# Choosing the starter pokemon


def choose_starter(player):
    os.system('cls' if os.name == 'nt' else 'clear')
    stats()
    print(f"{bcolors.OKGREEN}{board}{bcolors.ENDC}")
    print("Every Pokemon trainer has to choose their starter Pokemon,")
    print("before they go on their wonderfull journey trying to catch all Pokemon.")
    print(player["name"], "which one would you like to choose?\n")
    for pokemon in items:
        if pokemon["starter"] == True:
            print(pokemon["id"], pokemon["name"], end=" ")
    starter = input('\n\nWhich number?')
    if starter == '1' or starter == '2' or starter == '3':
        starter = int(starter)
        for pokemon in items:
            if pokemon["starter"] == True:
                if pokemon["id"] == starter:
                    player["collected_pokemon"].append(pokemon)
                    print(pokemon["name"], "is your new best friend!!")
    else:
        input("you have to pick a starter!")
        choose_starter(player)


# Taking the steps on the board


def waiting_screen(rand_int, player):
    for i in range(0, rand_int):
        player["location"] = player["location"] + 1
        loop_board(player)
        player["place_on_board"] = places[player["location"]]
        print_board()
        time.sleep(0.5)


# Every turn of the game


def turn(player):
    print(f"{bcolors.OKBLUE}\n\n\n Throw the dice{bcolors.ENDC}",
          player["name"], f"{bcolors.OKBLUE}? (enter){bcolors.ENDC}")
    input()
    rand_int = random.randint(1, 6)
    waiting_screen(rand_int, player)
    print(f"{bcolors.OKBLUE}Turn{bcolors.ENDC}", player["name"], ":",
          rand_int, "places", "\n")
    special_square(player)

    input("\n(enter)")

    print_board()
    print(f"{bcolors.OKBLUE}Turn{bcolors.ENDC}", player["name"], ":",
          rand_int, "places", "\n")

    if player == player1:
        turn(player2)
    else:
        turn(player1)

# start of the game


def start_of_game():
    choose_starter(player1)
    input("\n(enter)")
    choose_starter(player2)
    input("\n(enter)")

    os.system('cls' if os.name == 'nt' else 'clear')
    stats()
    print(f"{bcolors.OKGREEN}{board}{bcolors.ENDC}")
    turn(player1)


explain()
start_of_game()

questions.close()
