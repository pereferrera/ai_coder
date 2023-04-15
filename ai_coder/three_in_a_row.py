
"""
Implementation of the classic three-in-a-row game.
"""
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
            print('Invalid input')


def check_winner():
    """
    Checks if someone has won the game by checking for three-in-a-row.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] and row[1] == row[2] and row[0] is not None:
            return row[0]
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    # Check diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]


def game_over():
    """
    Checks if the game is over by checking for a winner or a full board.
    """
    if check_winner() is not None:
        print(f'{check_winner()} won!')
        return True
    for row in board:
        for cell in row:
            if cell is None:
                return False
    print('The game is a draw!')
    return True


def machine_turn():
    """
    Generates a random valid move and places the machine symbol on the board.
    """
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] is None:
            board[row][col] = machine_symbol
            break


# Main loop
while True:
    print_board()
    user_turn()
    if game_over():
        break
    machine_turn()
    if game_over():
        break
