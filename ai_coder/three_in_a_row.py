
"""
Implementation of the classic three-in-a-row game.

import random

# Representation of the board
board = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]

# User symbol
user_symbol = 'X'

# Machine symbol
machine_symbol = 'O'

def print_board():
    """
    Prints a visual representation of the board.
    """
    for row in board:
        print(row)

def user_turn():
    """
    Gets user input and places their symbol on the board.
    """
    while True:
        try:
            row, col = input('Your turn! Enter row, column: ').split(',')
            row, col = int(row), int(col)
            if board[row][col] is None:
                board[row][col] = user_symbol
                break
            else:
                print('This place is taken!')
        except (IndexError, ValueError):
            print('Invalid input