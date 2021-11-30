### This file will attempt to construct all possible boards given some constraints

#standard imports
import numpy as np
from classes import *

#create a label board
labels = labelBoard()

#load our example game board
game = gameBoard()
game.load('SavedBoards/branchingTreeBoard')

stats = game.stats
print(stats)
# print('\n Game Board for Testing')
# game.prettyPrint()

#apply board preprocessing (check for 0 voltorbs, check characteristic sums)
voltorbCheck(game, labels)  # check for 0 voltorb rows and columns
charSumCheckAuto(game, labels)  # calculate characteristic sums of rows and columns
print('\n Label Board after Preprocessing')
labels.prettyPrint()

#recursive board finding function
#find element with fewest possibilities (and choose the upper left one).

def searchBoardPossibilities(labels):
    numCasesMin = 4
    knownSquares = 0
    idx = (0,0)
    for i in range(0,5):
        for j in range(0,5):
            numCases = len(labels.map[i,j])
            if not numCases == 1: #skip all elements which are known
                if numCases < numCasesMin: #if number of possible cases less than current minimum cases
                    numCasesMin = numCases
                    idx = (i,j)
            else: #and increment the known squares counter
                knownSquares += 1
    return idx, numCasesMin, knownSquares

#returns list of new boards
def createBranch(labels):
    idxBranch, numCases, knownSquares = searchBoardPossibilities(labels) #find an element to branch on
    # print('\nBranching on element '+str(idxBranch))
    cases = labels.map[idxBranch] #what are the possible cases for that element
    newBoards = []
    for case in cases:
        newBoard = labelBoard() #create new instance of labelBoard
        newBoard.map[:] = labels.map[:] #copy over previous node's map (DON'T FORGET THE [:] or you will assign the two variables to each other!)
        newBoard.map[idxBranch] = case #set the branching case to one of the possibilities
        newBoards.append(newBoard) #append the new board to the list of new boards
        # print('\n New Board')
        # newBoard.prettyPrint()
    return newBoards

#returns list of valid boards
def validate(mystats, boardList):
    validFlag = np.ones(len(boardList),)
    for iii, board in enumerate(boardList):
            for i, row in enumerate(board.map):
                # print('\n Row '+str(i)+': '+str(row))
                knownCounter = 0
                for elem in row:
                    # print(elem)
                    if len(elem) == 1:
                        # print('This element is known')
                        knownCounter += 1
                # print(str(knownCounter) + ' elements in row '+str(i)+' are known')
                if knownCounter == 4:
                    keepFlag = 0
                    # print('Row '+str(i)+' can be solved')
                    rowSum = mystats[0][i] #pull stats for row i
                    rowVoltorbs = mystats[1][i] #pull stats for row i
                    # print('Row Sum: ' + str(rowSum))
                    # print('Row Voltorbs: '+str(rowVoltorbs))

                    #which element is still unknown?
                    idxSolve = 0
                    for j, elem in enumerate(row):
                        if not len(elem) == 1:
                            idxSolve = j

                    #for the unknown element, consider each case
                    for case in row[idxSolve]:
                        ptsCounter = 0 #init a points counter for this row
                        voltorbCounter = 0 #init a voltorbs counter for this row

                        for elem2 in row:
                            if len(elem2) == 1:
                                ptsCounter += int(elem2) #add up the total points in the row
                                if elem2 == '0':
                                    voltorbCounter += 1 #and the total voltorbs
                        ptsCounter += int(case) #don't forget to include the points/voltorbs from the case
                        if case == '0':
                            voltorbCounter += 1

                        # print('Assuming element '+str(idxSolve)+' of row '+str(i)+' is '+str(case)+' there are '+str(ptsCounter)+' points and '+str(voltorbCounter)+' voltorbs accounted for')
                        #check if this matches the true rowSum and rowVoltorbs
                        if ptsCounter == rowSum and voltorbCounter == rowVoltorbs:
                            keepFlag = 1
                            keepRow = row
                            keepRow[idxSolve] = case
                            board.map[i,:] = keepRow
                            # print(keepRow)
                    if keepFlag == 0:
                        # print('\nDelete this Board')
                        # board.prettyPrint()
                        validFlag[iii] = 0
                        break
                    # if keepFlag == 1:
                        # print('\nKeep this board')
                        # board.prettyPrint()
            #Do the same for columns
            for i, col in enumerate(board.map.T):
                # print('\n Col '+str(i)+': '+str(col))
                knownCounter = 0
                for elem in col:
                    # print(elem)
                    if len(elem) == 1:
                        # print('This element is known')
                        knownCounter += 1
                # print(str(knownCounter) + ' elements in col '+str(i)+' are known')
                if knownCounter == 4:
                    keepFlag = 0
                    # print(‘Col '+str(i)+' can be solved')
                    colSum = mystats[2][i]  # pull stats for col i
                    colVoltorbs = mystats[3][i]  # pull stats for col i
                    # print(‘Col Sum: ' + str(colSum))
                    # print(‘Col Voltorbs: '+str(colVoltorbs))

                    # which element is still unknown?
                    idxSolve = 0
                    for j, elem in enumerate(col):
                        if not len(elem) == 1:
                            idxSolve = j

                    # for the unknown element, consider each case
                    for case in col[idxSolve]:
                        ptsCounter = 0  # init a points counter for this col
                        voltorbCounter = 0  # init a voltorbs counter for this col

                        for elem2 in col:
                            if len(elem2) == 1:
                                ptsCounter += int(elem2)  # add up the total points in the col
                                if elem2 == '0':
                                    voltorbCounter += 1  # and the total voltorbs
                        ptsCounter += int(case)  # don't forget to include the points/voltorbs from the case
                        if case == '0':
                            voltorbCounter += 1

                        # print('Assuming element '+str(idxSolve)+' of col '+str(i)+' is '+str(case)+' there are '+str(ptsCounter)+' points and '+str(voltorbCounter)+' voltorbs accounted for')
                        # check if this matches the true colSum and colVoltorbs
                        if ptsCounter == colSum and voltorbCounter == colVoltorbs:
                            keepFlag = 1
                            keepCol = col
                            keepCol[idxSolve] = case
                            board.map[:, i] = keepCol
                            # print(keepCol)
                    if keepFlag == 0:
                        # print('\nDelete this Board')
                        # board.prettyPrint()
                        validFlag[iii] = 0
                        break
                    # if keepFlag == 1:
                    #     print('\nKeep this board')
                    #     board.prettyPrint()

    numBoards = len(boardList)
    for i in range(0,numBoards):
        idx = numBoards-i-1
        if validFlag[idx] == 0:
            del boardList[idx]
        #     print('Board '+str(idx)+' Deleted')
        # else:
        #     print('Board '+str(idx)+' Kept')
    return boardList

def isSolved(board):
    isSolved = 1
    for i in range(0,5):
        for j in range(0,5):
            if not len(board.map[i,j]) == 1:
                isSolved = 0
                return isSolved
    return isSolved

def branchBoards(mystats, parent_board, solved_boards):
    if isSolved(parent_board):
        solved_boards.append(parent_board)
    else:
        children = validate(mystats, createBranch(parent_board))
        for child_board in children:
             branchBoards(mystats, child_board, solved_boards)
    return solved_boards

# #From node, create branch
# newBoards = createBranch(labels)
# #delete invalid boards
# newBoards = validate(stats, newBoards)

solved_boards = branchBoards(stats, labels, [])

print('\nRemaining Boards\n')
for i, board in enumerate(solved_boards):
    print('Board '+str(i))
    board.prettyPrint()

