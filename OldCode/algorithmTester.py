import numpy as np
from boardClasses import *

def prettyPrint(map):
    totalLen = 5
    for row in map:
        printline = ''
        for elemf in row:
            elem = str(elemf)
            printline = printline + elem
            for k in range(0, totalLen - len(elem)):
                printline = printline + ' '
        # print(printline)

def charSumCheckAuto(game, labels): #check characteristic sum of
    stats = game.stats
    charRow, charCol = newCharEq(labels, stats)
    for i, val in enumerate(charRow): #for each row
        cases = possibilities(val) #find possible cases
        if cases == [(0, 0)]:  # if there are no 2 or 3 tiles, eliminate that row
            labels.elim('row', i)
        if cases == [(1, 0)]:  # if there can only be a 2 tile in the row, mark it as such
            labels.updateRow('3', i)

    for i, val in enumerate(charCol): #for each column
        cases = possibilities(val) #find possible tile cases
        if cases == [(0, 0)]:  # if there are no 2 or 3 tiles, eliminate that column
            labels.elim('col', i)
        if cases == [(1, 0)]:  # if there can only be a 2 tile in the column, mark it as such
            labels.updateCol('3', i)
    return charRow, charCol

def voltorbCheck(game, labels): #perform automatic revealing of all rows with 0 voltorbs (using dummyBoard as game)
    stats = game.stats
    for i, val in enumerate(stats[1]):
        if val == 0:
#             # print('Row number ' + str(i) + ' is safe')
            reveal(game, labels, 'row', i)
    # check for 0 voltorb columns
    for i, val in enumerate(stats[3]):
        if val == 0:
#             # print('Col number ' + str(i) + ' is safe')
            reveal(game, labels, 'col', i)

def remainingTiles(labels): #how many unknown tiles remain?
    tiles_row = []
    tiles_col = []
    for row in labels.map:
        remain_rows = 5
        for elem in row:
            if len(elem) == 1:
                remain_rows = remain_rows - 1
        tiles_row.append(remain_rows)
    for col in labels.map.T:
        remain_cols = 5
        for elem in col:
            if len(elem) == 1:
                remain_cols = remain_cols - 1
        tiles_col.append(remain_cols)

    return tiles_row, tiles_col


#calculate row figure of Merit
def FOMMat(game, labels):
    charRow, charCol = charSumCheckAuto(game, labels)
    rowVoltorbs = game.stats[1]
    colVoltorbs = game.stats[3]
    # rowRemaining, colRemaining = remainingTiles(labels)
    rowFom = charRow/(1+rowVoltorbs)
    colFom = charCol/(1+colVoltorbs)
    fomMat = np.round(np.outer(rowFom,colFom),2)
    for i in range(0,5):
        for j in range(0,5):
            if len(labels.map[i,j]) == 1:
                fomMat[i,j] = 0
    return fomMat

def isComplete(game, labels):
    totalCards = 0
    revealedCards = 0
    for i in range(0,5):
        for j in range(0,5):
            gameElem = game.map[i,j]
            labelElem = labels.map[i,j]

            #if 2s are correctly found
            if gameElem == 2:
                totalCards += 1
                if int(labelElem) == 2:
                    revealedCards += 1
            #if 3s are correctly found
            if gameElem == 3:
                totalCards += 1
                if int(labelElem) == 3:
                    revealedCards += 1

    if totalCards == revealedCards:
        complete = 1
    else:
        complete = 0
    return complete


def playGame():

    successFlag = 0

    #create dummy board
    game = dummyBoard(initflag = 1)
    #game.save('TestingBoard')
    # game.load('TestingBoard')
    # print('\n True Board')
    # game.prettyPrint()

    #create label board
    labels = labelBoard()

    #Preprocess Board (0 voltorb check and charsum)
    voltorbCheck(game, labels) #check for 0 voltorb rows
    charSumCheckAuto(game, labels) #calculate characteristic sums
    # print('\n Initial Label Board')
    # labels.prettyPrint()

    termin = 25
    for i in range(0,termin):
        #recheck board
        charSumCheckAuto(game, labels)  # calculate characteristic sums
        completeFlag = isComplete(game,labels)
        if completeFlag:
            # print('\n')
            # print('============================')
            # print('GAME IS COMPLETE')
            # print('============================')
            successFlag = 1
            break

        # print('\n')
        # print('============================')
        # print('Choice Number '+str(i))
        # print('============================')
        #calculate FOM board
        fom = FOMMat(game, labels)
        # print('\n FoM Board')
        # prettyPrint(fom)

        #find maximum FoM
        fomMax = np.max(np.max(fom))
        idxs = zip(*np.where(fom == fomMax))
        choice = list(idxs)[0]

        #choose that element
        result = revealElem(game,labels,choice[0],choice[1])

        # print('Element Chosen: ' +str(choice))
        # print('Result: '+ str(result))
        # print('\n Label Board')
        # labels.prettyPrint()

        if result == 0:
            successFlag = 0
            # print('============================')
            # print('FAILURE FAILURE FAILURE FAILURE')
            # print('============================')
            break


    return successFlag

successes = []
trials = 1000
for i in range(0,trials):
    successes.append(playGame())

winrate = 100*sum(successes)/len(successes)
print('Win Rate: '+str(winrate)+'%')


