#! python3

# GAME CONSTANTS
EMPTY = 10
X = 1
O = 0


class Helper:
    @classmethod
    def utility(cls, board: list):
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
        return False  # the game is not yet finished

    @classmethod
    def turn(cls, board: list):
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

    @classmethod
    def possible_actions(cls, board: list):
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

    @classmethod
    def transition(cls, board: list, action: tuple, max_turn=True):
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

    @classmethod
    def maximizer(cls, board: list, dumb=False):
        """
        Recursive function. Returns action with the highest possible outcome.

        Parameters
        ---------
        board: list
            current or hypothetical board state
        dumb: bool
            decides whether the AI will let the player win or not
        """
        if Helper.utility(board) is not False:
            return Helper.utility(board), None
        result = None
        if not dumb:
            v = -2
        if dumb:
            v = 1000
        for action in Helper.possible_actions(board):
            v2 = Helper.minimizer(Helper.transition(board, action))
            if not dumb:
                if v2[0] >= v:
                    result = action
                    v = v2[0]
            if dumb:
                if v2[0] <= v:
                    result = action
                    v = v2[0]
            board[action[0]][action[1]] = EMPTY
        return v, result

    @classmethod
    def minimizer(cls, board: list, dumb=False):
        """
        Recursive function. Returns action with the lowest possible outcome.

        Parameters
        ----------
        board: list
            current or hypothetical board state
        dumb: bool
            decides whether the AI will let the player win or not
        """
        if Helper.utility(board) is not False:
            return Helper.utility(board), None
        result = None
        if not dumb:
            v = 1000
        else:
            v = -2
        for action in Helper.possible_actions(board):
            v2 = Helper.maximizer(Helper.transition(board, action, max_turn=False))
            if not dumb:
                if v2[0] <= v:
                    result = action
                    v = v2[0]
            if dumb:
                if v2[0] >= v:
                    result = action
                    v = v2[0]
            board[action[0]][action[1]] = EMPTY
        return v, result

    @classmethod
    def player(cls, board: list, max_player=True, dumb=False):
        """
        Returns best move either for X or O

        Parameters
        ----------
        board: list
            current state of the board
        max_player: bool
            True if the AI is playing max, False otherwise
        dumb: bool
            decides whether the AI will let the player win or not
        """
        if max_player:
            return Helper.maximizer(board, dumb)[1]
        else:
            return Helper.minimizer(board, dumb)[1]

    @classmethod
    def move(cls, board: list, action: tuple, max_player=True):
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

    # UTILITY GAME FUNCTIONS
    @classmethod
    def player_select(cls):
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

    @classmethod
    def get_coordinates(cls):
        """Gets coordinates to draw the X/O."""
        print('Enter coords:')
        s = input()
        if s == '':
            exit()
        y, x = s.split()
        y, x = int(y), int(x)
        return y, x

    @classmethod
    def print_board(cls, board: list):
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

    @classmethod
    def valid(cls, board: list, position: tuple):
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

    @classmethod
    def game_over(cls, board: list, max_player=True):
        """
        Checks the state of the game.

        Parameters
        ----------
        board: list
            current state of the board
        max_player: bool
            True if the AI is playing max, False otherwise
        """
        res = Helper.utility(board)
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

