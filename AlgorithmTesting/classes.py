import numpy as np

#THIS METHOD SHOULD ONLY BE USED IF THE GAMEBOimport numpy as np

#define constants for board generation
#probabilities chosen to have average of 25 points, with 12 voltorbs per board.
#probabilities for level 8
probV = 0.40 #probability of voltorb tile
prob3 = 0.176 #probability of three tile
prob2 = 0.176 #probability of two tile

# #probabilities for level 4
# probV = 0.368 #probability of voltorb tile
# prob3 = 0.112 #probability of three tile
# prob2 = 0.144 #probability of two tile

# #probabilities for level 2
# probV = 0.28 #probability of voltorb tile
# prob3 = 0.08 #probability of three tile
# prob2 = 0.12 #probability of two tile


class gameBoard: #voltorb flip board class, generates a full game of voltorb flip

    def __init__(self):
        self.map = np.empty((5, 5)) #create the board map
        self.makeRandomBoard() #generate a randomized, valid voltorb flip board

    def select(self, probV = probV, prob2 = prob2, prob3 = prob3):  #encodes probability distribution for voltorbs, 3 tiles, and 2 tiles
        seed = np.random.rand(1)
        if seed > probV + prob2 + prob3:
            return 3
        elif seed > probV + prob2:
            return 2
        elif seed > probV:
            return 0
        else:
            return 1

    def makeRandomBoard(self): #generate random voltorb flip board
        for i, row in enumerate(self.map): #for each element
            for j, elem in enumerate(row):
                self.map[i,j] = self.select() #choose an element according to the probability distribution
        self.calcstats() #calculate the relevant statistics (sum of points in row, sum of points in column, voltorbs in row, etc)

    def calcstats(self): #calculates total points and voltorbs in each row and column
        rowPoints = np.sum(self.map,axis=1,dtype=int)
        colPoints = np.sum(self.map,axis=0,dtype=int)
        rowVoltorbs = 5 - np.count_nonzero(self.map,axis = 1) #counts number of elements labeled zero
        colVoltorbs = 5 - np.count_nonzero(self.map, axis=0) #counts number of elements labeled zero
        self.stats = rowPoints, rowVoltorbs, colPoints, colVoltorbs #store statistics as tuple

    def save(self, name): #save the board map
        np.save(name,self.map)

    def load(self, name): #load the board map and calculate relevant statistics
        self.map = np.load(name+'.npy')
        self.calcstats()

    # def prettyPrint(self): #print the board to console in an aesthetically pleasing way
    #     print('\n'.join(['\t'.join([str(int(cell)) for cell in row]) for row in self.map]))
    def prettyPrint(self): #print the label board in an aesthetically pleasing way
        totalLen = 5
        for row in self.map:
            printline = ''
            for elem in row:
                printline = printline+str(int(elem))
                for k in range(0,totalLen-len(str(int(elem)))):
                    printline = printline + ' '
            print(printline)

class labelBoard: #class for containing possible values of gameBoard. tiles contain some subset of '0','1','2','3' stored in a string

    def __init__(self): #optionally inherit another label board
        self.map = np.empty((5, 5), dtype=np.dtype('U100'))
        self.map[:] = '0123' #in each tile, put all possible values in a string

    def elimElem(self, mystring, i, j): #eliminate a single possibility stored in mystring ('0', '1', etc) from an element
        elem = self.map[i,j]
        newelem = elem.replace(mystring,'') #replace the value, i.e. '2' with '', removing it from the tile string
        self.map[i,j] = newelem

    def elimRow(self, mystring, rownum): #eliminate a single possibility ('0', '1', etc) from a row
        row = self.map[rownum,:]
        for i,elem in enumerate(row):
            if not len(row[i])==1:
                row[i] = elem.replace(mystring,'')
        self.map[rownum,:] = row

    def elimCol(self, mystring, colnum): #eliminate a single possibility ('0', '1', etc) from a column
        col = self.map[:,colnum]
        for i,elem in enumerate(col):
            if not len(col[i]) == 1:
                col[i] = elem.replace(mystring,'')
        self.map[:,colnum] = col

    def elim(self, rowOrCol, num): #shorthand for eliminating both 2s and 3s from either rows or columns
        if rowOrCol == 'row':
            self.elimRow('2',num)
            self.elimRow('3', num)
        elif rowOrCol == 'col':
            self.elimCol('2', num)
            self.elimCol('3', num)

    def set(self, mystring, i, j): #set the i,jth element to be mystring
        self.map[i,j] = mystring

    def prettyPrint(self): #print the label board in an aesthetically pleasing way
        totalLen = 5
        for row in self.map:
            printline = ''
            for elem in row:
                printline = printline+elem
                for k in range(0,totalLen-len(elem)):
                    printline = printline + ' '
            print(printline)

#standalone functions
def possibilities(charSum): #take characteristic sum of a row, Σ+V-5, return possibilities for (# 2 tiles, # 3 tiles)
    if charSum == 0:
        return [(0,0)]
    if charSum == 1:
        return [(1,0)]
    if charSum == 2:
        return [(2,0), (0,1)]
    if charSum == 3:
        return [(3,0), (1,1)]
    if charSum == 4:
        return [(4,0), (2,1), (0,2)]
    if charSum == 5:
        return [(5,0), (3,1), (1,1)]
    if charSum == 6:
        return [(4,1), (2,2), (0,3)]
    if charSum == 7:
        return [(3,2), (1,3)]
    if charSum == 8:
        return [(2,3), (0,4)]
    if charSum == 9:
        return [(1, 4)]
    if charSum == 10:
        return[(0,5)]

def charSum(stats):  # calculate naive (no information) characteristic sum for rows and cols
    charRow = stats[0] + stats[1] - 5
    charCol = stats[2] + stats[3] - 5
    return charRow, charCol

def newCharEq(labels, stats):  #calculate characteristic sum including information from known tiles

    # load statistics of gameboard
    rowSum = stats[0]
    rowVoltorbs = stats[1]
    colSum = stats[2]
    colVoltorbs = stats[3]

    # calculate old (no information) characteristic sum
    charRow = rowSum + rowVoltorbs - 5
    charCol = colSum + colVoltorbs - 5

    # for every known element that's a two, subtract 1 from the characteristic sum,
    # for every known element that's a three, subtract 2
    # known elements are defined as strings having length 1 in the label board
    # iterate over rows and columns
    for i in range(0, 5):
        row = labels.map[i, :]
        for j in range(0, 5):
            elem = row[j]
            if len(elem) == 1:
                if int(elem) == 2:
                    charRow[i] = charRow[i] - 1
                elif int(elem) == 3:
                    charRow[i] = charRow[i] - 2
    for j in range(0, 5):
        col = labels.map[:, j]
        for i in range(0, 5):
            elem = col[i]
            if len(elem) == 1:
                if int(elem) == 2:
                    charCol[j] = charCol[j] - 1
                elif int(elem) == 3:
                    charCol[j] = charCol[j] - 2

    return charRow, charCol

def revealElem(game, labels, i,j): #label the i,jth element of the label board according to the game board
    val = int(game.map[i,j])
    labels.set(str(val),i,j)
    return val

def reveal(game, labels, rowOrCol, num): #shorthand for revealing entire row or column
    if rowOrCol == 'row':
        for j in range(0,5):
            revealElem(game, labels,num,j)
    elif rowOrCol == 'col':
        for i in range(0,5):
            revealElem(game, labels,i,num)

#THIS METHOD SHOULD BE USED IF THE TRUE BOARD IS NOT KNOWN TO THE COMPUTER (uses only the board stats, not the board itself)
def charSumCheck(stats, labels): #check characteristic sum of rows and columns. If
    charRow, charCol = newCharEq(labels, stats) #calculate characteristic sum of rows and columns, including all known information
    for i, val in enumerate(charRow): #for each row
        cases = possibilities(val) #find the possibilities for containing 2 or 3 tiles
        if cases == [(0, 0)]: #if there are no 2 or 3 tiles, eliminate that row
            labels.elim('row', i)
        if cases == [(1,0)]:#if there can only be a 2 tile in the row, mark it as such
            labels.elimRow('3', i)
    for i, val in enumerate(charCol): #for each column
        cases = possibilities(val) #find the possibilities for containing 2 or 3 tiles
        if cases == [(0, 0)]: #if there are no 2 or 3 tiles, eliminate that column
            labels.elim('col', i)
        if cases == [(1, 0)]: #if there can only be a 2 tile in the column, mark it as such
            labels.elimCol('3',i)
    return charRow, charCol

#THIS METHOD SHOULD BE USED IF THE ENTIRE GAME BOARD IS AVAILABLE -- THIS IS FOR ALGORITHM TESTING, USES THE GAMEBOARD OBJECT
def charSumCheckAuto(game, labels): #check characteristic sum of
    stats = game.stats
    charRow, charCol = newCharEq(labels, stats)
    for i, val in enumerate(charRow): #for each row
        cases = possibilities(val) #find possible cases
        if cases == [(0, 0)]:  # if there are no 2 or 3 tiles, eliminate that row
            labels.elim('row', i)
        if cases == [(1, 0)]:  # if there can only be a 2 tile in the row, mark it as such
            labels.elimRow('3', i)
    for i, val in enumerate(charCol): #for each column
        cases = possibilities(val) #find possible tile cases
        if cases == [(0, 0)]:  # if there are no 2 or 3 tiles, eliminate that column
            labels.elim('col', i)
        if cases == [(1, 0)]:  # if there can only be a 2 tile in the column, mark it as such
            labels.elimCol('3', i)
    return charRow, charCol

#THIS METHOD SHOULD ONLY BE USED IF THE GAMEBOARD IS AVAILABLE AND KNOWN TO THE COMPUTER -- FOR ALGORITHM TESTING
def voltorbCheck(game, labels): #perform automatic revealing of all rows with 0 voltorbs
    stats = game.stats
    for i, val in enumerate(stats[1]): #check for rows with 0 voltorbs
        if val == 0:
            reveal(game, labels, 'row', i) #reveal those rows
    for i, val in enumerate(stats[3]): #check for columns with 0 voltorbs
        if val == 0:
            reveal(game, labels, 'col', i) #reveal those columns

def updateKnown(game,labels): #update known elements from gameboard into labelboard
    for i in range(0,5):
        for j in range(0,5):
            if not game.map[i,j] == 'X':
                # print(game.map[i,j])
                labels.map[i,j] = game.map[i,j]

def mark(labels): #mark all '01' spaces in the labelboard with '-' for easier reading
    for i in range(0,5):
        for j in range(0,5):
            if labels.map[i,j] == '01':
                labels.map[i,j] = '-'

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

def voltorbCheck(game, labels): #perform automatic revealing of all rows with 0 voltorbs
    stats = game.stats
    for i, val in enumerate(stats[1]): #check for rows with 0 voltorbs
        if val == 0:
            reveal(game, labels, 'row', i) #reveal those rows
    for i, val in enumerate(stats[3]): #check for columns with 0 voltorbs
        if val == 0:
            reveal(game, labels, 'col', i) #reveal those columns

def updateKnown(game,labels): #update known elements from gameboard into labelboard
    for i in range(0,5):
        for j in range(0,5):
            if not game.map[i,j] == 'X':
                # print(game.map[i,j])
                labels.map[i,j] = game.map[i,j]

def mark(labels): #mark all '01' spaces in the labelboard with '-' for easier reading
    for i in range(0,5):
        for j in range(0,5):
            if labels.map[i,j] == '01':
                labels.map[i,j] = '-'

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

#THIS METHOD SHOULD ONLY BE USED IF THE GAMEBOARD IS AVAILABLE AND KNOWN TO THE COMPUTER -- FOR ALGORITHM TESTING
def FOM(game, labels): #calculate figure of merit matrix
    charRow, charCol = charSumCheckAuto(game, labels) #find characteristic sum of rows and columns
    rowVoltorbs = game.stats[1] #get number of voltorbs in rows
    colVoltorbs = game.stats[3] #get number of voltorbs in columns
    rowFom = charRow/(1+rowVoltorbs) #calculate the figure of merit for each row
    colFom = charCol/(1+colVoltorbs) #calculate the figure of merit for each column
    # rowFom = charRow / (1 )  # calculate the figure of merit for each row
    # colFom = charCol / (1 )  # calculate the figure of merit for each column
    fomMat = np.round(np.outer(rowFom,colFom),2) #take the outer product of these two vectors to create a matrix
    #set all elements with known values to 0 FOM
    for i in range(0,5):
        for j in range(0,5):
            if len(labels.map[i,j]) == 1:
                fomMat[i,j] = 0
    return fomMat

#THIS METHOD SHOULD ONLY BE USED IF THE GAMEBOARD IS AVAILABLE AND KNOWN TO THE COMPUTER -- FOR ALGORITHM TESTING
def isComplete(game, labels): #checks if the board has been completely solved
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

#function definitions
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

def isLineSolvable(line): #check how many uniquely known elements a row/column has, and return the index of the last unknown element
    knownCounter = 0
    idxSolve = 0
    for j, elem in enumerate(line):  # how many elements in the row are uniquely known?
        if len(elem) == 1:
            knownCounter += 1
        if not len(elem) == 1:  # store the latest index of a not-uniquely-known element
            idxSolve = j  # if i'm in a solvable row (4 known elements), this index will point to the only unknown element
    return knownCounter, idxSolve

#returns list of valid boards
def validate(mystats, boardList):

    validFlag = np.ones(len(boardList),)
    for iii, board in enumerate(boardList):
            for i, row in enumerate(board.map):

                knownCounter, idxSolve = isLineSolvable(row) #check if the row is solvable
                if knownCounter == 4: #if the row can be solved (4 unique elements
                    keepFlag = 0
                    rowSum = mystats[0][i] #pull stats for row i
                    rowVoltorbs = mystats[1][i] #pull stats for row i

                    for case in row[idxSolve]: #for the unknown element, consider each possibility
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

                        #check if this matches the true rowSum and rowVoltorbs
                        if ptsCounter == rowSum and voltorbCounter == rowVoltorbs:
                            keepFlag = 1
                            keepRow = row
                            keepRow[idxSolve] = case
                            board.map[i,:] = keepRow

                    if keepFlag == 0: #flag board for deletion, invalid board
                        validFlag[iii] = 0
                        break

            for i, col in enumerate(board.map.T):

                knownCounter, idxSolve = isLineSolvable(col)
                if knownCounter == 4:
                    keepFlag = 0
                    colSum = mystats[2][i]  # pull stats for col i
                    colVoltorbs = mystats[3][i]  # pull stats for col i

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

                        # check if this matches the true colSum and colVoltorbs
                        if ptsCounter == colSum and voltorbCounter == colVoltorbs:
                            keepFlag = 1
                            keepCol = col
                            keepCol[idxSolve] = case
                            board.map[:, i] = keepCol

                    if keepFlag == 0: #Flag board for deletion
                        validFlag[iii] = 0
                        break

    #iterate (backwards) through list of boards and delete all boards that have been flagged for deletion
    numBoards = len(boardList)
    for i in range(0,numBoards):
        idx = numBoards-i-1
        if validFlag[idx] == 0:
            del boardList[idx]
    return boardList

#is the board solved? i.e. are all elements uniquely known?
def isSolved(board):
    isSolved = 1
    for i in range(0,5):
        for j in range(0,5):
            if not len(board.map[i,j]) == 1:
                isSolved = 0
                return isSolved
    return isSolved

#recursive function that creates the branching tree
def branchBoards(mystats, parent_board, solved_boards): #takes board statistics, a parent board, and a list of solved boards
    if isSolved(parent_board): #if the parent board is solved
        solved_boards.append(parent_board) #add it to the list of solved boards
    else: #otherwise
        children = validate(mystats, createBranch(parent_board)) #branch out more boards from the parent board, and check if they're invalid
        for child_board in children: #for each child board
             branchBoards(mystats, child_board, solved_boards) #recall the branching function
    return solved_boards #return the list of solved boards

def integerizeBoards(boardList): #store all solved label boards as game boards (with integers instead of strings) for easier calculation
    newBoardList = []
    for board in boardList:
        newBoard = gameBoard()
        for i in range(0,5):
            for j in range(0,5):
                newBoard.map[i,j] = int(board.map[i,j])
        newBoard.calcstats()
        newBoardList.append(newBoard)
    return newBoardList

def tileProbabilities(solved_board_list): #takes list of solved boards as gameBoard object (integer elements)
    numBoards = len(solved_board_list)
    metaBoard = np.zeros((5, 5, 4)) #i, j, probability
    for gameBoard in solved_board_list:
        for i in range(0,5):
            for j in range(0,5):
                if gameBoard.map[i,j] == 0:
                    metaBoard[i,j,0] += 1/numBoards
                elif gameBoard.map[i,j] == 1:
                    metaBoard[i,j,1] += 1/numBoards
                elif gameBoard.map[i,j] == 2:
                    metaBoard[i,j,2] += 1/numBoards
                elif gameBoard.map[i,j] == 3:
                    metaBoard[i,j,3] += 1/numBoards
    return metaBoard

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

#THIS METHOD RETURNS the FOM board using a probabilistic branching algorithm, but if that fails (recursion depth), falls back on the naive algorithm
def FOMProbabilistic(game, labels): #tries the probabilistic branching tree algorithm first, if the recursion depth is exceeded, uses th naive algorithm.
    stats = game.stats
    try:
        # print('\nTrying to construct all boards')
        solved_boards = branchBoards(stats, labels, [])
        solved_boards_int = integerizeBoards(solved_boards)
        probabilityBoard = tileProbabilities(solved_boards_int)
        # print('\nRemaining Boards: ' + str(len(solved_boards_int)))
        for i, board in enumerate(solved_boards_int):
            checksum = np.sum(np.asarray(stats) - np.asarray(board.stats))
            if not checksum == 0:
                print('THIS BOARD IS INVALID (SOMEHOW)')
        fomBoard = (probabilityBoard[:, :, 2] + 2 * probabilityBoard[:, :, 3]) / (1 + probabilityBoard[:, :, 0])
        # set all elements with known values to 0 FOM
        for i in range(0, 5):
            for j in range(0, 5):
                if len(labels.map[i, j]) == 1:
                    fomBoard[i, j] = 0
        naive = 0
    except RecursionError:
        print('Recursion Depth Exceeded, using Naive Algorithm')
        fomBoard = FOM(game,labels)
        solved_boards_int = 0
        probabilityBoard = 0
        naive = 1

    return fomBoard, solved_boards_int, probabilityBoard, naive


#The full function for playing a game of voltorb flip, with or without the branching tree solution algorithm
def playVoltorbFlip(branching = 0): #play a game of voltorb flip, using the algorithm, and return success or failure
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
        if branching:
            fom, _, _, naive = FOMProbabilistic(game, labels) #construct figure of merit matrix
        else:
            fom = FOM(game, labels) #construct figure of merit matrix
        fomMax = np.max(np.max(fom)) #find maximum figure of merit
        idxs = zip(*np.where(fom == fomMax)) #find indices of maximum figure of merits on board (can be multiple)
        choice = list(idxs)[0] #choose the upper left one
        result = revealElem(game,labels,choice[0],choice[1]) #reveal that element
        if result == 0: #if you hit a voltorb
            successFlag = 0 #you lose
            break

    return successFlag
