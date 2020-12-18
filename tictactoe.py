#! python3
# Cleaner draft, moved viable functions from draft file.

EMPTY = 10
X = 1
O = 0


def utility(board: list):
    """
    Returns value of the board.

    Parameters
    ----------
    board: list
        current or hypothetical board state
    """
    transpose = list(map(list, zip(*board)))  # Transposed copy of the board
    counts = 0
    diagonal_a = sum(board[z][z] for z in range(3))
    diagonal_b = sum([board[2][0], board[1][1], board[0][2]])
    for i in range(3):
        # Checking vertical and horizontal terminal states
        if sum(board[i]) == 3 or sum(transpose[i]) == 3:
            return 1
        if sum(board[i]) == 0 or sum(transpose[i]) == 0:
            return -1
        if 10 not in board[i]:
            counts += 1
    # Checking diagonal terminal states
    if diagonal_a == 3 or diagonal_b == 3:
        return 1
    if diagonal_a == 0 or diagonal_b == 0:
        return -1
    if counts == 3:
        return 0
    return False # the game is not yet finished


def turn(board: list):
    """
    Returns True if it's max's turn, False otherwise.

    Parameters
    ----------
    board: list
        current or hypothetical board state
    """
    counts = 0
    for row in board:
        for item in row:
            if not item == 10:
                counts += 1
    if counts % 2 == 1:
        return False
    return True


def possible_actions(board: list):
    """
    Returns list of possible moves/actions.

    Parameters
    ----------
    board: list
        current or hypothetical board state
    """
    coords = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                coords.append((i, j))
    return coords


def transition(board: list, action: tuple, max_turn=True):
    """
    Returns resulting board after making a certain move.

    Parameters
    ----------
    board: list
        current or hypothetical board state
    action: tuple
        y and x coordinates
    max_turn: bool
        True if it's max's turn, False otherwise
    """
    y, x = action
    if max_turn:
        board[y][x] = 1
    else:
        board[y][x] = 0
    return board


def maximizer(board: list):
    """
    Recursive function. Returns action with the highest possible outcome.

    Parameters
    ---------
    board: list
        current or hypothetical board state
    """
    if utility(board) is not False:
        return utility(board), None
    result = None
    v = -2
    for action in possible_actions(board):
        v2 = minimizer(transition(board, action))
        if v2[0] >= v:
            result = action
            v = v2[0]
        board[action[0]][action[1]] = EMPTY
    return v, result


def minimizer(board: list):
    """
    Recursive function. Returns action with the lowest possible outcome.

    Parameters
    ----------
    board: list
        current or hypothetical board state
    """
    if utility(board) is not False:
        return utility(board), None
    result = None
    v = 1000
    for action in possible_actions(board):
        v2 = maximizer(transition(board, action, max_turn=False))
        if v2[0] <= v:
            result = action
            v = v2[0]
        board[action[0]][action[1]] = EMPTY
    return v, result


def player(board: list, max_player=True):
    """
    Returns best move either for X or O

    Parameters
    ----------
    board: list
        current state of the board
    max_player: bool
        True if the AI is playing max, False otherwise
    """
    if max_player:
        return maximizer(board)[1]
    else:
        return minimizer(board)[1]


def move(board: list, action: tuple, max_player=True):
    """
    Makes a movement of the board in place.

    Parameters
    ---------
    board: list
        current state of the board
    action: tuple
        y and x coordinates
    max_player: bool
        True if the AI is playing max, False otherwise
    """
    y, x = action
    if max_player:
        board[y][x] = 1
    else:
        board[y][x] = 0


# UTILITY GAME FUNCTIONS

def player_select():
    """Gets user choice for playing X or O."""
    print('Which player would you like to be? [O/X])')
    p = input()
    if p.lower() == 'o':
        return True
    elif p.lower() == 'x':
        return False
    else:
        print('Invalid input, please try again later.')
        exit()


def get_coordinates():
    """Gets coordinates to draw the X/O."""
    print('Enter coords:')
    s = input()
    if s == '':
        exit()
    y, x = s.split()
    y, x = int(y), int(x)
    return y, x


def print_board(board: list):
    """
    Prints board on each turn.

    Parameters
    ----------
    board: list
        current state of the board
    """
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                print(' ', end='|')
            elif board[i][j] == X:
                print('X', end='|')
            else:
                print('O', end='|')
        print()
    print()


def valid(board: list, position: tuple):
    """
    Returns True if the given move is valid, False otherwise.

    Parameters
    ----------
    board: list
        current state of the board
    position: tuple
        y and x coordinates
    """
    y, x = position
    if not board[y][x] == EMPTY:
        print('INVALID COORDINATES, PLEASE TRY AGAIN')
        return False
    return True


def game_over(board: list, max_player=True):
    """
    Checks the state of the game.

    Parameters
    ----------
    board: list
        current state of the board
    max_player: bool
        True if the AI is playing max, False otherwise
    """
    res = utility(board)
    if res is not False:
        if res == 0:
            exit('TIE')

        if max_player:
            if res == 1:
                exit('AI WON')
            if res == -1:
                exit('YOU WON')
        else:
            if res == 1:
                exit('YOU WON')
            if res == -1:
                exit('AI WON')


def main():
    """TEXT BASED DEMO OF THE TIC-TAC-TOE"""
    grid = [[EMPTY for i in range(3)] for j in range(3)]
    ai = player_select()
    while True:
        game_over(grid, ai)
        if ai:
            if not turn(grid):
                y, x = get_coordinates()
                if not valid(grid, (y, x)):
                    continue
                grid[y][x] = 0
            else:
                ac = player(grid, max_player=ai)
                move(grid, ac, max_player=ai)
        else:
            if turn(grid):
                y, x = get_coordinates()
                if not valid(grid, (y, x)):
                    continue
                grid[y][x] = 1
            else:
                ac = player(grid, max_player=ai)
                move(grid, ac, max_player=ai)
        print_board(grid)


main()
