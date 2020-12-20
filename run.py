#! python3

from tictactoe import Helper

# CONSTANTS
EMPTY = 10
O = 0
X = 1


def main():
    """TEXT BASED VERSION OF THE TIC-TAC-TOE"""
    grid = [[EMPTY for i in range(3)] for j in range(3)]
    ai = Helper.player_select()
    while True:
        Helper.game_over(grid, ai)
        if ai:
            if not Helper.turn(grid):
                y, x = Helper.get_coordinates()
                if not Helper.valid(grid, (y, x)):
                    continue
                grid[y][x] = O
            else:
                ac = Helper.player(grid, max_player=ai)
                Helper.move(grid, ac, max_player=ai)
        else:
            if Helper.turn(grid):
                y, x = Helper.get_coordinates()
                if not Helper.valid(grid, (y, x)):
                    continue
                grid[y][x] = X
            else:
                ac = Helper.player(grid, max_player=ai)
                Helper.move(grid, ac, max_player=ai)
        Helper.print_board(grid)


main()