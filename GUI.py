#! python3

import pygame
import random
from tictactoe import Helper

pygame.init()

# CONSTANTS
EMPTY = 10
X = 1
O = 0
MODIFIER = 200
clumsy = False


class Game:
    """
    Game class.

    Parameters
    ----------
    screen: pygame.Surface
        game window

    Attributes
    ----------
    screen: pygame.Surface
        game window
    board: list
        tic-tac-toe board
    max_player: bool
        True if the user plays X, False otherwise
    """
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.board = [[EMPTY for i in range(3)] for j in range(3)]
        self.max_player = None

    def change_player(self, t: bool):
        """Changes max_player depending on the user's choice."""
        self.max_player = t

    def draw_window(self):
        """Draws the tic-tac-toe board on the game window."""
        for i in range(200, 600, 200):
            pygame.draw.line(self.screen, "black", (i, 130), (i, 670), width=3)
        for j in range(300, 700, 200):
            pygame.draw.line(self.screen, "black", (30, j), (570,  j), width=3)

        pygame.display.flip()

    @staticmethod
    def player_select():
        """Displays player_select "interface" to the user."""
        font = pygame.font.SysFont('comicsans', 40, True)
        text = font.render("Choose your player:", 1, (0, 0, 0))
        text2 = font.render("Press 1 for X, 2 for O", 1, (0, 0, 0))
        window.blit(text, (150, 20))
        window.blit(text2, (150, 60))
        pygame.display.flip()

    @staticmethod
    def clear_top():
        """Clears the top side of the screen."""
        temp = pygame.Surface((600, 100))
        temp.fill((255, 255, 255))
        window.blit(temp, (0, 0))
        pygame.display.flip()

    def draw_o(self, coordinates: tuple):
        """
        Draws a circle (O) to the screen at the given position.

        Parameters
        ----------
        coordinates: tuple
            y, x coordinates
        """
        y, x = coordinates
        x_pos, y_pos = 100, 200  # default position for coordinates (0, 0)
        x_pos += MODIFIER * x
        y_pos += MODIFIER * y
        pygame.draw.circle(self.screen, (0, 0, 0), (x_pos, y_pos), 80, width=3)
        pygame.display.flip()

    def draw_x(self, coordinates: tuple):
        """
        Draws an X to the screen at the given position.

        Parameters
        ----------
        coordinates: tuple
            y, x coordinates
        """
        # Default positions for coordinates (0, 0)
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
        """Updates the screen depending on the state of the board."""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == X:
                    self.draw_x((i, j))
                if self.board[i][j] == O:
                    self.draw_o((i, j))

    def game_over(self):
        """Checks for terminal state of the board."""
        font = pygame.font.SysFont("comicsans", 80, True)
        text = font.render('AI WON!', 1, (255, 0, 0))
        text1 = font.render('YOU WON!', 1, (0, 255, 0))
        area = (175, 20)
        over = False
        res = Helper.utility(self.board)
        if res is not False:
            if res == 0:
                text2 = font.render('TIE!', 1, (0, 0, 255))
                self.screen.blit(text2, (230, 20))
                over = True
            if self.max_player:
                if res == 1:
                    self.screen.blit(text1, area)
                    over = True
                if res == -1:
                    self.screen.blit(text, area)
                    over = True
            else:
                if res == 1:
                    self.screen.blit(text, area)
                    over = True
                if res == -1:
                    self.screen.blit(text1, area)
                    over = True
        pygame.display.flip()
        return over

    @staticmethod
    def get_pos(coordinates: tuple):
        """
        Calculates coordinates given the mouse-clicked position.

        Parameters
        ----------
        coordinates tuple
            y, x coordinates (screen scale)
        """
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


# Randomly chooses whether the AI will let the user win or not
n = random.randint(0, 1)
if n == 1:
    clumsy = True

# Set up
window = pygame.display.set_mode((600, 700))
window.fill((255, 255, 255))
pygame.display.flip()
pygame.display.set_caption("Tic Tac Toe")
test = Game(window)
test.draw_window()

# Player select "interface"
selected = False
while not selected:
    test.player_select()
    pygame.time.delay(200)
    test.clear_top()
    pygame.time.delay(200)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_2):
            selected = True
            if event.key == pygame.K_1:
                test.change_player(True)
            elif event.key == pygame.K_2:
                test.change_player(False)

# Ai plays max or min depending on the user's choice
if test.max_player:
    ai = False
else:
    ai = True

# Main game loop
running = True
finished = False
while running:

    test.update_board()
    finished = test.game_over()

    if Helper.turn(test.board) == ai and not finished:
        ac = Helper.player(test.board, dumb=clumsy, max_player=ai)
        Helper.move(test.board, ac, max_player=ai)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not finished:
            p = Game.get_pos(event.pos)
            if Helper.turn(test.board) == test.max_player:
                if not Helper.valid(test.board, p):
                    continue
                if test.max_player:
                    test.board[p[0]][p[1]] = X
                else:
                    test.board[p[0]][p[1]] = O
