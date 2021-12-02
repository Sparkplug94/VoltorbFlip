### This file tests the Voltorb Flip Solutions algorithm by generating a random Voltorb Flip board, and using the algorithm to solve it. It prints the win rate of the algorithm

#standard imports
import numpy as np
from classes import *
from tqdm import tqdm

#check the recursion limit
import sys
print(sys.getrecursionlimit())
#set the recursion limit to 5k
sys.setrecursionlimit(5000)

def prettyPrint(map):
    totalLen = 5
    for row in map:
        printline = ''
        for elemf in row:
            elem = str(elemf)
            printline = printline + elem
            for k in range(0, totalLen - len(elem)):
                printline = printline + ' '
        print(printline)

def playVoltorbFlip(): #play a game of voltorb flip, using the algorithm, and return success or failure
    successFlag = 0 #set successflag
    game = gameBoard() #create random gameboard
    labels = labelBoard()  #create label board
    voltorbCheck(game, labels)  # check for 0 voltorb rows and columns
    charSumCheckAuto(game, labels)  # calculate characteristic sums of rows and columns

    #THIS IS THE VOLTORB FLIP SOLUTION ALGORITHM
    maxSteps = 25 #maximum number of steps for algorithm is number of tiles
    for i in range(0,maxSteps):
        charSumCheckAuto(game, labels)  # calculate characteristic sums
        completeFlag = isComplete(game,labels) #check if game is complete
        if completeFlag: #if it's complete, set successFlag to 1
            successFlag = 1
            break
        #fom, _, _, naive = FOMProbabilistic(game, labels) #construct figure of merit matrix
        fom = FOM(game, labels) #construct figure of merit matrix
        fomMax = np.max(np.max(fom)) #find maximum figure of merit
        idxs = zip(*np.where(fom == fomMax)) #find indices of maximum figure of merits on board (can be multiple)
        choice = list(idxs)[0] #choose the upper left one
        result = revealElem(game,labels,choice[0],choice[1]) #reveal that element
        if result == 0: #if you hit a voltorb
            successFlag = 0 #you lose
            break

    return successFlag

successes = []
trials = 3000
for i in tqdm(range(0,trials)): #run X trials
    # print('Trial '+str(i))
    flag = playVoltorbFlip()
    successes.append(flag)
    # if flag:
    #     print('Success')
    # else:
    #     print('Failure')

winrate = 100*sum(successes)/len(successes) #print win rate
print('\n\nSuccess Rate: '+str(winrate)+'%')
