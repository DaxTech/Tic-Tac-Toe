#! python3
# Draft to test functionality, loading grid and validating input from the user.
import pprint
import sys


grid = [[None for i in range(3)] for i in range(3)]

# TODO
# Build the logic of the game (when someone wins, when there's tie, etc.)

print(*grid, sep='\n')
print()


def win(board):
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

def max(board):
    pass

def min(board):
    pass






