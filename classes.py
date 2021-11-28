import numpy as np

#define constants for board generation
#probabilities chosen to have average of 25 points, with 12 voltorbs per board.
probV = 0.48 #probability of voltorb tile
prob3 = 0.08 #probability of three tile
prob2 = 0.32 #probability of two tile

class gameBoard: #voltorb flip board class, generates a full game of voltorb flip

    def __init__(self):
        self.map = np.empty((5, 5)) #create the board map
        self.makeRandomBoard() #generate a randomized, valid voltorb flip board

    def select(probV=probV, prob2=prob2, prob3=prob3):  #encodes probability distribution for voltorbs, 3 tiles, and 2 tiles
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

    def prettyPrint(self): #print the board to console in an aesthetically pleasing way
        print('\n'.join(['\t'.join([str(int(cell)) for cell in row]) for row in self.map]))


class labelBoard: #class for containing possible values of gameBoard. tiles contain some subset of '0','1','2','3' stored in a string

    def __init__(self):
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

#THIS METHOD SHOULD BE USED IF THE BOAD IS NOT KNOWN TO THE COMPUTER (uses only the board stats, not the board itself)
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

#THIS METHOD SHOULD ONLY BE USED IF THE GAMEBOimport numpy as np

#define constants for board generation
#probabilities chosen to have average of 25 points, with 12 voltorbs per board.
probV = 0.48 #probability of voltorb tile
prob3 = 0.08 #probability of three tile
prob2 = 0.32 #probability of two tile

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

    def prettyPrint(self): #print the board to console in an aesthetically pleasing way
        print('\n'.join(['\t'.join([str(int(cell)) for cell in row]) for row in self.map]))


class labelBoard: #class for containing possible values of gameBoard. tiles contain some subset of '0','1','2','3' stored in a string

    def __init__(self):
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

#THIS METHOD SHOULD BE USED IF THE BOAD IS NOT KNOWN TO THE COMPUTER (uses only the board stats, not the board itself)
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

def FOMMat(game, labels): #calculate figure of merit matrix
    charRow, charCol = charSumCheckAuto(game, labels) #find characteristic sum of rows and columns
    rowVoltorbs = game.stats[1] #get number of voltorbs
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