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

stats = np.load('OCRstats.npy') #load stats from OCRmain

game = importBoard(stats) #create game board using stats
rowVoltorbs = stats[1]
colVoltorbs = stats[3]

# load data into game board
tmp = np.asarray([['X', 'X', 'X', '1', 'X'],
                  ['X', 'X', 'X', '3', 'X'],
                  ['X', 'X', 'X', '1', 'X'],
                  ['X', 'X', 'X', '2', 'X'],
                  ['X', 'X', 'X', '3', '2']],dtype=np.dtype('U100'))

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
# mark(labels)

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
print('Row Points: '+str(stats[0]))
print('Row Voltorbs: '+str(stats[1]))
print('Row Points: '+str(stats[2]))
print('Row Points: '+str(stats[3]))

print('\n FoM Matrix')
prettyPrint(fomMat)

#find maximum FoM
fomMax = np.max(np.max(fomMat))
idxs = zip(*np.where(fomMat == fomMax))
choice = list(idxs)[0]
print('\n You should choose '+str(choice))