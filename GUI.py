#! python3

import pygame

pygame.init()

EMPTY = 10
X = 1
O = 0
MODIFIER = 200

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
        board[y][x] = X
    else:
        board[y][x] = O


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

class Game:
    """Game class."""
    def __init__(self, screen):
        self.screen = screen
        self.board = [[EMPTY for i in range(3)] for j in range(3)]
        self.max_player = None

    def change_player(self, t):
        self.max_player = t

    def draw_window(self):
        for i in range(200, 600, 200):
            pygame.draw.line(self.screen, "black", (i, 130), (i, 670), width=3)
        for j in range(300, 700, 200):
            pygame.draw.line(self.screen, "black", (30, j), (570,  j), width=3)

        pygame.display.flip()

    def player_select(self):
        font = pygame.font.SysFont('comicsans', 40, True)
        text = font.render("Choose your player:", 1, (0, 0, 0))
        text2 = font.render("Press 1 for X, 2 for O", 1, (0, 0, 0))
        window.blit(text, (150, 20))
        window.blit(text2, (150, 60))
        pygame.display.flip()

    def clear_top(self):
        temp = pygame.Surface((600, 100))
        temp.fill((255, 255, 255))
        window.blit(temp, (0, 0))
        pygame.display.flip()

    def draw_o(self, coordinates):
        y, x = coordinates
        x_pos, y_pos = 100, 200
        x_pos += MODIFIER * x
        y_pos += MODIFIER * y
        pygame.draw.circle(self.screen, (0, 0, 0), (x_pos, y_pos), 80, width=3)
        pygame.display.flip()

    def draw_x(self, coordinates):
        x_min, x_max = 25, 165
        y_min, y_max = 130, 270
        y, x = coordinates
        x_min += MODIFIER * x
        x_max += MODIFIER * x
        y_min += MODIFIER * y
        y_max += MODIFIER * y

        pygame.draw.line(self.screen, (0, 0, 0), (x_min, y_min), (x_max, y_max), width=3)
        pygame.draw.line(self.screen, (0, 0, 0), (x_max, y_min), (x_min, y_max), width=3)
        pygame.display.flip()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 1:
                    self.draw_x((i, j))
                if self.board[i][j] == 0:
                    self.draw_o((i, j))

    def game_over(self):
        font = pygame.font.SysFont("comicsans", 80, True)
        text = font.render('AI WON', 1, (255, 0, 0))
        text1 = font.render('YOU WON', 1, (0, 255, 0))
        area = (150, 20)
        res = utility(self.board)
        if res is not False:
            if res == 0:
                text2 = font.render('TIE', 1, (0, 0, 255))
                self.screen.blit(text2, area)
            if self.max_player:
                if res == 1:
                    self.screen.blit(text1, area)
                if res == -1:
                    self.screen.blit(text, area)
            else:
                if res == 1:
                    self.screen.blit(text, area)
                if res == -1:
                    self.screen.blit(text1, area)
        pygame.display.flip()

    @staticmethod
    def get_pos(coordinates):
        x_coords, y_coords = coordinates
        x_pos, y_pos = None, None
        if y_coords in range(100, 300):
            y_pos = 0
        elif y_coords in range(300, 500):
            y_pos = 1
        elif y_coords in range(500, 700):
            y_pos = 2
        if x_coords in range(0, 200):
            x_pos = 0
        elif x_coords in range(200, 400):
            x_pos = 1
        elif x_coords in range(400, 600):
            x_pos = 2
        return y_pos, x_pos


window = pygame.display.set_mode((600, 700))
window.fill((255, 255, 255))
pygame.display.flip()
pygame.display.set_caption("Tic Tac Toe")
test = Game(window)
test.draw_window()

selected = False
while not selected:
    test.player_select()
    pygame.time.delay(200)
    test.clear_top()
    pygame.time.delay(200)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            selected = True
            if event.key == pygame.K_1:
                test.change_player(True)
            elif event.key == pygame.K_2:
                test.change_player(False)


if test.max_player:
    ai = False
else:
    ai = True

running = True
finished = False
while running:

    test.update_board()
    test.game_over()

    try:
        if turn(test.board) == ai:
            ac = player(test.board, max_player=ai)
            move(test.board, ac, max_player=ai)
    except:
        continue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            p = Game.get_pos(event.pos)
            if turn(test.board) == test.max_player:
                if not valid(test.board, p):
                    continue
                if test.max_player:
                    test.board[p[0]][p[1]] = 1
                else:
                    test.board[p[0]][p[1]] = 0
