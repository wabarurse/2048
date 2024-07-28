"""By Hasan and richard
2048 is a single player game with a 4 by 4 grid. 
You start of with 2 numbers and slide the number, and combine matching numbers to eventually reach 2048!
A new number is generated after every move is made.
This game also has different versions including Fruit Bowl, Traffic Jam, and Zoo Mania, which use emojis that slide and combine into eachother.
Have fun!
"""
#Just make it so that it moves first then adds the number
import random
import math
import copy
import time
from typing import List

global four_added
four_added = 0

WINNING_NUMBER = "2048"

original = {"0": "       ", "2": "   2   ", "4": "   4   ", "8": "   8   ", "16": "   16  ", "32": "   32  ",
            "64": "   64  ", "128": "  128  ", "256": "  256  ", "512": "  512  ", "1024": "  1024 ",
            "2048": "  2048 "}
fruit_bowl = {"0": "🔳", "2": "🍎", "4": "🍊", "8": "🍋", "16": "🍐", "32": "🍒", "64": "🍇", "128": "🍈", "256": "🍉",
              "512": "🫐", "1024": "🍑", "2048": "🍌"}
traffic_jam = {"0": "🔳", "2": "🚗", "4": "🚕", "8": "🚙", "16": "🚌", "32": "🚎", "64": "🚜", "128": "🚓", "256": "🚑",
               "512": "🚒", "1024": "🚐", "2048": "🚔"}
zoo = {"0": "🔳", "2": "🐔", "4": "🐧", "8": "🐤", "16": "🐸", "32": "🐰", "64": "🦊", "128": "🐻", "256": "🐼",
       "512": "🐻‍❄️", "1024": "🐯", "2048": "🐵"}


def delay(time_milli):
    """Delays the program in milliseconds"""
    time.sleep(time_milli / 1000)


def reset_board() -> [[str]]:
    """Returns a 4x4 matrix with strings of 0"""
    board = [["0", "0", "0", "0"],
             ["0", "0", "0", "0"],
             ["0", "0", "0", "0"],
             ["0", "0", "0", "0"]]

    return board


def print_board(board: [[str]], game_type: dict):
    """
    Prints a 4 by 4 shaped board with line characters outlining the board and separating each column and row. 
    Takes each string in game_board, and takes the value of that string in the dictionary game_type, 
    and prints it inside each of each spot on the board, row by row.

    """
    counter = 0
    print("┌────────┬────────┬────────┬────────┐")
    for i in board:
        print("│        │        │        │        │")
        print("│", end=" ")
        for j in i:
            print(game_type[j], end="│ ")
        print()
        print("│        │        │        │        │")
        if counter != 3:
            print("├────────┼────────┼────────┼────────┤")
            counter += 1
    print("└────────┴────────┴────────┴────────┘")


def print_emote_board(board:[[str]], game_type: dict):
    """
    Prints a 4 by 4 shaped board with blank emoji squares outlining the board. 
    Takes each string in game_board, and takes the value of that string in the dictionary game_type, 
    and prints it inside each of each spot on the board, row by row.
    """
    counter = 0
    print("⬜⬜⬜⬜⬜⬜")
    for i in board:
        print("⬜", end="")
        for j in i:
            print(game_type[j], end="")
        print("⬜", end="")
        print()
    print("⬜⬜⬜⬜⬜⬜")


def get_largest_number(board:[[str]]) -> str:
    """
    Finds and returns the largest number in the matrix
    """
    largest = int(board[0][0])

    for i in range(len(board)):
        for j in board[i]:
            if int(j) > largest:
                largest = int(j)

    return str(largest)


def calc_score(board:[[str]]) -> int:
    """
    Gets the score by using the math formula, 
    number * (log_2_number)-1, this formula applies to every number that is not 0, and all values get added together to make the score.

    32
    >>>128
    256
    >>> 1792
    """

    global four_added

    total = 0
    for i in (board):
        for j in i:
            num = int(j)
            if num != 0:
                total += num * ((math.log(num, 2)) - 1)
    total = round(total) - (four_added * 4)
    return total


def spot_empty(board:[[str]], row: int, col: int) -> bool:
    """
    Checks if a spot on the board is empty,
    Returns bool True if empty, or bool False if occupied.
    """
    if board[row][col] == "0":
        return True
    else:
        return False


def get_move(prompt: str) -> str:
    """
    Makes sure that all moves are valid
    Only accepts W, A, S and D (converts the input to capital)
    Once the move is valid it returns it
    """
    while True:
        move = str(input(prompt))
        move = move.upper()

        if move == "W" or move == "A" or move == "S" or move == "D" or move == "QUIT":
            return move
        else:
            print("Invalid choice")


def choose_number() -> str:
    """
    Chooses 2 and 4
    90% chance to generate a 2 and a 10% chance to generate a 4
    """
    global four_added

    pick_number = random.randint(0, 9)

    if pick_number == 0:
        four_added += 1
        return "4"
    else:
        return "2"



def choose_spot(board:[[str]]):
    """
    Picks a random square in the matrix and makes sure its empty
    If it is empty, get a random number and place it into that square
    """
    while True:
        row = random.randint(0, 3)
        col = random.randint(0, 3)

        if spot_empty(board, row, col):
            number = choose_number();
            board[row][col] = number
            break


def shift_left(numbers: list) -> list:
    """
    Shifts all non zero numbers in an array to the left

    shift_left([0,4,2,0])
    >>> [4,2,0,0]
    """
    temp = []

    for j in numbers:
        if j != "0":
            temp.append(j)

    for h in range(4 - len(temp)):
        temp.append("0")

    return temp


def shift_right(numbers: list) -> list:
    """
    Shifts all non zero numbers in an array to the right

    shift_right([0,4,2,0])
    >>> [0,0,4,2]
    """
    temp = []

    for j in numbers:
        if j != "0":
            temp.append(j)

    for h in range(4 - len(temp)):
        temp.insert(h, "0")

    return temp


def combine(numbers: list):
    """
    Takes a list and if any two adjacent numbers are identitcal, they get combined

    combine([0,2,2,0])
    >>> [0,4,0,0]
    """

    for n in range(4):
        if n != 3:
            if numbers[n] == numbers[n + 1]:
                numbers[n] = str(int(numbers[n]) * 2)
                numbers[n + 1] = "0"


def choose_move(board, move) -> [[str]]:
    """
    Asks the user to input a move, and then runs the moving function depending on if they enter w, a, s, or d
    Depending on their input, this function changes the game_board respectively
    """
    while True:
        shifted_list = []
        finished_list = []

        if move == "A":
            for i in range(len(board)):

                shifted_list = shift_left(board[i])
                combine(shifted_list)
                finished_list = shift_left(shifted_list)

                for k in range(4):
                    board[i][k] = finished_list[k]

                shifted_list = []
                finished_list = []

            return board

        elif move == "D":
            for i in range(len(board)):

                shifted_list = shift_right(board[i])
                combine(shifted_list)
                finished_list = shift_right(shifted_list)

                for k in range(4):
                    board[i][k] = finished_list[k]

                shifted_list = []
                finished_list = []

            return board

        elif move == "W":
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[j][i] != "0":
                        shifted_list.append(board[j][i])

                for h in range(4 - len(shifted_list)):
                    shifted_list.append("0")

                combine(shifted_list)
                finished_list = shift_left(shifted_list)

                for k in range(4):
                    board[k][i] = finished_list[k]

                shifted_list = []
                finished_list = []

            return board

        elif move == "S":

            for i in range(len(board)):
                for j in range(len(board)):
                    if board[j][i] != "0":
                        shifted_list.append(board[j][i])

                for h in range(4 - len(shifted_list)):
                    shifted_list.append("0")

                combine(shifted_list)
                finished_list = shift_right(shifted_list)

                for k in range(4):
                    board[k][i] = finished_list[k]

                shifted_list = []
                finished_list = []

            return board


def predict(board, move="GAME") -> bool:
    """
    Default: checks if the game is over by chekcing if there are any possible moves
    Else: Check is game_board has changed after a move
    If it is changed return False, if it hasnt changed return True
    """
    original_board = board

    if move == "GAME":
        if choose_move(copy.deepcopy(original_board), "W") == original_board and choose_move(copy.deepcopy(original_board), "A") == original_board and choose_move(copy.deepcopy(original_board), "S") == original_board and choose_move(
            copy.deepcopy(original_board), "D") == original_board:
            return True
        else:
            return False

    if move == "W":
        if choose_move(copy.deepcopy(original_board), "W") == original_board:
            return True
        else:
            return False

    if move == "A":
        if choose_move(copy.deepcopy(original_board), "A") == original_board:
            return True
        else:
            return False
    if move == "S":
        if choose_move(copy.deepcopy(original_board), "S") == original_board:
            return True
        else:
            return False
    if move == "D":
        if choose_move(copy.deepcopy(original_board), "D") == original_board:
            return True
        else:
            return False


def main():
    global four_added
    win_loss = []
    scores = []
    option = "0"
    print("\033[1m" + "Welcome to 2048\n")
    print("\x1B[3m" + "By Hasan And Richard" + "\x1B[0m\n")
    print("Enter the number beside an option to select it.\n")
    while option != "4":
        four_added = 0
        score = 0
        game_choice = "0"
        print("\x1B[3m" + "Which what you like to do?" + "\x1B[0m\n""""
  1) Play
  2) See Statistics
  3) Recieve Help
  4) Leave
        """)

        option = str(input("> "))
        if option == "1":
            while game_choice != "5":
                print("\x1B[3m" + "Which gamemode would you like to play?" + "\x1B[0m")
                print("""
  1) Original
  2) Fruit Bowl
  3) Traffic Jam
  4) Zoo Mania
  5) Go Back
                """)

                game_choice = input("> ")

                if game_choice == "1" or game_choice == "2" or game_choice == "3" or game_choice == "4":
                    four_added = 0
                    game_board = reset_board()
                    choose_spot(game_board)
                    choose_spot(game_board)
                    while True:

                        score = calc_score(game_board)
                        board_before_move = copy.deepcopy(game_board)
                        calc_score(game_board)

                        if game_choice == "1":
                            print('\t\t\033[1m' + "2048" + '\033[0m')
                            print("\t    Your Score: {}".format('\033[1m' + str(score) + '\033[0m'))
                            print_board(game_board, original)
                        elif game_choice == "2":
                            print('     \033[1m' + "2048" + '\033[0m')
                            print(" Your Score: {}".format('\033[1m' + str(score) + '\033[0m'))
                            print_emote_board(game_board, fruit_bowl)
                        elif game_choice == "3":
                            print('     \033[1m' + "2048" + '\033[0m')
                            print(" Your Score: {}".format('\033[1m' + str(score) + '\033[0m'))
                            print_emote_board(game_board, traffic_jam)
                        elif game_choice == "4":
                            print('     \033[1m' + "2048" + '\033[0m')
                            print(" Your Score: {}".format('\033[1m' + str(score) + '\033[0m'))
                            print_emote_board(game_board, zoo)
                        move = get_move("> ").upper()

                        if move == "QUIT":
                            print("Thank you for playing!\n")
                            scores.append(score)

                            break

                        game_board = choose_move(game_board, move)

                        if get_largest_number(game_board) == WINNING_NUMBER:
                            calc_score(game_board)

                            if game_choice == "1":
                                print('\t\t\033[1m' + "2048" + '\033[0m')
                                print("\t    Your Score: {}".format('\033[1m' + str(score) + '\033[0m'))
                                print_board(game_board, original)
                            elif game_choice == "2":
                                print('     \033[1m' + "2048" + '\033[0m')
                                print(" Your Score: {}".format('\033[1m' + str(score) + '\033[0m'))
                                print_emote_board(game_board, fruit_bowl)
                            elif game_choice == "3":
                                print('     \033[1m' + "2048" + '\033[0m')
                                print(" Your Score: {}".format('\033[1m' + str(score) + '\033[0m'))
                                print_emote_board(game_board, traffic_jam)
                            elif game_choice == "4":
                                print('     \033[1m' + "2048" + '\033[0m')
                                print(" Your Score: {}".format('\033[1m' + str(score) + '\033[0m'))
                                print_emote_board(game_board, zoo)

                            print("You have won!")
                            win_loss.append("W")
                            scores.append(score)
                            break

                        else:
                            if not predict(board_before_move, move):
                                choose_spot(game_board)
                            if predict(board_before_move):
                                print("YOU LOST")
                                win_loss.append("L")
                                scores.append(score)
                                break

                elif game_choice == "5":
                    break


        elif option == "2":
            print("Your Attemps (W = win, L = loss):", win_loss)
            print("Your Past Scores: ", scores)
            print()
            delay(3000)
        elif option == "3":
            print("Use the wasd keys to shift the board up, left, down and right respectively.")
            print("Tiles with the same number/icon merge into one when they touch. Add them up to reach 2048 (or the icon representing 2048)!")
            print("There are four game modes to chose from, the original has numbers and the others have emojis!")
            print("Enter the number beside an option to select it.")
            print()

            delay(3000)
        elif option =="4":
            print("Bye Bye Bozo!!!!     (⌐■_■)–︻╦╤─   \(✖╭╮✖)/")
            print("                  Hasan(Mafia Boss)  You(Noob)")

if __name__ == '__main__':
    main()
#Leave cursor 