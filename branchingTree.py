### This file will attempt to construct all possible boards given some constraints

#standard imports
import numpy as np
from classes import *

#check the recursion limit
import sys
print(sys.getrecursionlimit())
#set the recursion limit to 5k
sys.setrecursionlimit(10000)

#create a label board
labels = labelBoard()

#load our example game board
game = gameBoard()
game.save('SavedBoards/branchingTreeBoard2')
print('\n Voltorb Flip Board')
game.prettyPrint()
print('Row Points: ' + str(game.stats[0]))
print('Row Voltorbs: ' + str(game.stats[1]))
print('Col Points: ' + str(game.stats[2]))
print('Col Voltorbs: ' + str(game.stats[3]))

stats = game.stats
# print(stats)
# print('\n Game Board for Testing')
# game.prettyPrint()

#apply board preprocessing (check for 0 voltorbs, check characteristic sums)
voltorbCheck(game, labels)  # check for 0 voltorb rows and columns
charSumCheckAuto(game, labels)  # calculate characteristic sums of rows and columns
print('\n Label Board after Preprocessing')
labels.prettyPrint()

solved_boards_int, probabilityBoard, fomBoard, naive = FOMProbabilistic(game, labels)

print('\n FOM Board')
prettyPrint(np.round(fomBoard,2))

print('\n Game Board')
game.prettyPrint()