### This file tests the Voltorb Flip Solutions algorithm by generating a random Voltorb Flip board, and using the algorithm to solve it. It prints the win rate of the algorithm

#standard imports
import numpy as np
from classes import *
from tqdm import tqdm
import sys

#set the recursion limit to 5k
sys.setrecursionlimit(3000)

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

successes = []
trials = 300
branching = 1
realLevel2Board = 0

for i in tqdm(range(0,trials)): #run X trials of voltorb flip
    flag = playVoltorbFlip(branching = branching, realBoard = realLevel2Board)
    successes.append(flag)

winrate = 100*sum(successes)/len(successes) #print win rate
print('\n\nSuccess Rate: '+str(winrate)+'%')
