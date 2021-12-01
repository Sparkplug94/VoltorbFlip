import numpy as np
from OldCode.boardClasses import *

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

# stats = np.load('OCRstats.npy') #load stats from OCRmain
rowPoints = np.array([5,3,6,6,5])
rowVoltorbs = np.array([0,2,1,1,3])
colPoints = np.array([3,5,5,4,8])
colVoltorbs = np.array([2,1,2,2,0])
stats = rowPoints, rowVoltorbs, colPoints, colVoltorbs

game = importBoard(stats) #create game board using stats
rowVoltorbs = stats[1]
colVoltorbs = stats[3]

#load data into game board
tmp = np.asarray([['1', '1', '1', '1', '1'],
                  ['X', 'X', 'X', 'X', '1'],
                  ['X', '1', 'X', '2', '2'],
                  ['X', 'X', '3', 'X', '1'],
                  ['X', 'X', 'X', 'X', '3']],dtype=np.dtype('U100'))


# tmp = np.asarray([['X', 'X', 'X', 'X', 'X'],
#                   ['X', 'X', 'X', 'X', 'X'],
#                   ['X', 'X', 'X', 'X', 'X'],
#                   ['X', 'X', 'X', 'X', 'X'],
#                   ['X', 'X', 'X', 'X', 'X']],dtype=np.dtype('U100'))

#overwrite board
game.map = tmp

#create label board
labels = labelBoard()

#update known
updateKnown(game, labels)

#perform charsum check
charRow, charCol = charSumCheck(game.stats, labels)
#mark 01s with - for easier reading
mark(labels)

#calculate row figure of Merit
rowFom = charRow/(1+rowVoltorbs)
colFom = charCol/(1+colVoltorbs)
fomMat = np.round(np.outer(rowFom,colFom),1)
for i in range(0,5):
    for j in range(0,5):
        if len(labels.map[i,j]) == 1:
            fomMat[i,j] = 0

print('\n Board')
labels.prettyPrint()

print('\n FoM Matrix')
prettyPrint(fomMat)

#find maximum FoM
fomMax = np.max(np.max(fomMat))
idxs = zip(*np.where(fomMat == fomMax))
choice = list(idxs)[0]
print('You should choose '+str(choice))


possibilities