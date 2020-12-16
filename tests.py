#!python3
from copy import deepcopy
from clean_draft import *

grid = [[10,10,10],
        [10,10,10],
        [10,10,10]]

#print('Max\'s turn: '+ str(turn(grid)))
#print(utility(grid))
#print(possible_actions(grid))

print(*grid, sep='\n')
while True:
        res = utility(grid)
        if res is not False:
            if res == 1:
                exit('AI WON')
            if res == 0:
                exit('TIE')
            if res == -1:
                exit('YOU WON')
        if not turn(grid):
            print("Enter coords:")
            s = input()
            if s == '': exit()
            y,x = s.split()
            y,x =int(y), int(x)
            grid[y][x] = 0
        else:
            table = deepcopy(grid)
            val = max_value(table)
            y, x = val[1]
            grid[y][x] = 1

        print(*grid, sep='\n')


