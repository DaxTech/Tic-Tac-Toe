#! python3
# Draft to test functionality, loading grid and validating input from the user.
import pprint
import sys


grid = [[None for i in range(3)] for i in range(3)]

# TODO
# Build the logic of the game (when someone wins, when there's tie, etc.)

print(*grid, sep='\n')
print()


def results(board):
    """Returns numeric value depending on the state of the game."""
    temp = list(map(list, zip(*board)))
    diagonalA = sum(board[z][z] for z in range(3))
    diagonalB = sum([board[2][0], board[1][1], board[0][2]])
    for i in range(3):
        # We can refine these conditions later
        if sum(board[i]) == 3 or sum(temp[i]) == 3:
            return 1
        if sum(board[i]) == 0 or sum(temp[i]) == 0:
            return -1
        if diagonalA == 3 or diagonalB == 3:
            return 1
        if diagonalA == 0 or diagonalB == 0:
            return -1

    return 0

def turn(board):
    pass


def game_over(board):
    for i in board:
        if None in board:
            return False
    return True


def available_coords(board):
    coords = []
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                coords.append((i, j))

    return coords


def fill(board, x, y, max_turn):
    if max_turn:
        board[y][x] = 1
        return board
    else:
        board[y][x] = 0
        return board


def minimax(board, max_turn):
    if game_over(board):
        return results(board)

    if max_turn:
        for y, x in available_coords(board):
            board = fill(board, x, y, max_turn=True)






