#! python3
# Cleaner draft, moved viable functions from draft file.

grid = [[10 for i in range(3)] for i in range(3)]


def utility(board):
    """Returns value of the board."""
    # It's a bit clunky, it can surely be improved.
    temp = list(map(list, zip(*board)))
    c = 0
    diagonalA = sum(board[z][z] for z in range(3))
    diagonalB = sum([board[2][0], board[1][1], board[0][2]])
    for i in range(3):
        if sum(board[i]) == 3 or sum(temp[i]) == 3:
            return 1
        if sum(board[i]) == 0 or sum(temp[i]) == 0:
            return -1

        if 10 not in board[i]:
            c += 1

    if diagonalA == 3 or diagonalB == 3:
        return 1
    if diagonalA == 0 or diagonalB == 0:
        return -1
    if c == 3:
        return 0
    return False


def turn(board):
    """Returns True if it's max's turn, False otherwise."""
    counts = 0
    for row in board:
        for item in row:
            if not item == 10:
                counts += 1

    if counts % 2 == 1:
        return True
    else:
        return False


def possible_actions(board):
    """Returns list of possible moves/actions."""
    coords = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 10:
                coords.append((i, j))

    return coords


def transition(board, action, max_turn=True):
    y, x = action
    if max_turn:
        board[y][x] = 1
    else:
        board[y][x] = 0
    return board