import numpy as np

probV = 0.48 #probability of voltorb tile
prob3 = 0.08 #probability of three tile
prob2 = 0.32 #probability of two tile
#probabilities chosen to have average of 25 points, with 12 voltorbs per board.

#generate probability distribution
def select(probV = probV, prob2 = prob2, prob3 = prob3):
    seed = np.random.rand(1)
    if seed > probV+prob2+prob3:
        return 3
    elif seed > probV+prob2:
        return 2
    elif seed > probV:
        return 0
    else:
        return 1

#voltorb flip board class
class importBoard:
    def __init__(self, stats):
        self.map = np.empty((5,5), dtype=np.dtype('U100'))
        self.map[:]= 'X'
        self.stats = stats

    def save(self, name):
        np.savez(name, map = self.map, stats = self.stats)

    def load(self, name):
        npzfile = np.load(name+str('.npz'))
        self.map = npzfile['map']
        self.stats = npzfile['stats']

    def prettyPrint(self):
        totalLen = 5
        for row in self.map:
            printline = ''
            for elem in row:
                printline = printline+elem
                for k in range(0,totalLen-len(elem)):
                    printline = printline + ' '
            print(printline)


#voltorb flip dummy board
class dummyBoard:
    def __init__(self, initflag = 1): #initialize empty 5x5 array, fill with nans
        self.map = np.empty((5,5))
        self.map[:] = np.nan
        if initflag == 1:
            self.makeRandomBoard()

    def makeRandomBoard(self): #generate random voltorb flip board
        for i, row in enumerate(self.map):
            for j, elem in enumerate(row):
                self.map[i,j] = select()
        self.calcstats()

    def clearBoard(self): #generate random voltorb flip board
        self.map[:] = np.nan
        del self.stats
        del self.rowPoints
        del self.rowVoltorbs
        del self.colPoints
        del self.colVoltorbs

    def calcstats(self): #calculates total points and voltorbs in each row and column
        rowPoints = np.sum(self.map,axis=1,dtype=int)
        colPoints = np.sum(self.map,axis=0,dtype=int)
        rowVoltorbs = 5 - np.count_nonzero(self.map,axis = 1) #counts number of elements labeled zero
        colVoltorbs = 5 - np.count_nonzero(self.map, axis=0) #counts number of elements labeled zero
        self.rowPoints = rowPoints
        self.rowVoltorbs = rowVoltorbs
        self.colPoints = colPoints
        self.colVoltorbs = colVoltorbs
        self.stats = rowPoints, rowVoltorbs, colPoints, colVoltorbs

    def validate(self, mystats): #checks if stats of board matches mystats
        valid = True
        for elem in zip(mystats, self.stats):
            if not elem[0].all()==elem[1].all():
                valid=False
        return valid

    def save(self, name):
        np.save(name,self.map)

    def load(self, name):
        self.map = np.load(name+'.npy')
        self.calcstats()

    def prettyPrint(self):
        print('\n'.join(['\t'.join([str(int(cell)) for cell in row]) for row in self.map]))


class labelBoard: #class for labeling board

    def __init__(self):
        self.map = np.empty((5, 5), dtype=np.dtype('U100'))
        self.map[:] = '0123'

    def toSeed(self, string):
        arr = np.asarray(string.split(' '), dtype = np.dtype('U100'))
        print(arr)
        return arr

    def updateElem(self, elim, i, j): #eliminate a single possibility ('0', '1', etc) from an element
        elem = self.map[i,j]
        newelem = elem.replace(elim,'')
        self.map[i,j] = newelem

    def updateRow(self, elim, rownum): #eliminate a single possibility ('0', '1', etc) from a row
        row = self.map[rownum,:]
        for i,elem in enumerate(row):
            if not len(row[i])==1:
                row[i] = elem.replace(elim,'')
        self.map[rownum,:] = row

    def updateCol(self, elim, colnum): #eliminate a single possibility ('0', '1', etc) from a row
        col = self.map[:,colnum]
        for i,elem in enumerate(col):
            if not len(col[i]) == 1:
                col[i] = elem.replace(elim,'')
        self.map[:,colnum] = col

    def elim(self, rowOrCol, num): #shorthand for eliminating 2s and 3s from rows and columns
        if rowOrCol == 'row':
            self.updateRow('2',num)
            self.updateRow('3', num)
        elif rowOrCol == 'col':
            self.updateCol('2', num)
            self.updateCol('3', num)

    def choose(self, val, i, j): #choose the i,jth element to be val
        self.map[i,j] = val

    def prettyPrint(self):
        totalLen = 5
        for row in self.map:
            printline = ''
            for elem in row:
                printline = printline+elem
                for k in range(0,totalLen-len(elem)):
                    printline = printline + ' '
            print(printline)

def possibilities(charSum): #take characteristic sum Σ+V-5, return possibilities for (# 2 tiles, # 3 tiles)
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

def charEq(stats):  # calculate characteristic equation for rows and cols
    # print('Row Points ' + str(stats[0]))
    # print('Row Voltorbs ' + str(stats[1]))
    # print('Col Points ' + str(stats[2]))
    # print('Col Voltorbs ' + str(stats[3]))
    # print('Characteristic Equation: Σ+V-5 = #2 + 2 * #3')
    charRow = stats[0] + stats[1] - 5
    charCol = stats[2] + stats[3] - 5
    # print('Rows: ' + str(charRow))
    # print('Cols: ' + str(charCol))
    return charRow, charCol


def newCharEq(labels, stats):  # updates the characteristic sum with known information

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
    labels.choose(str(val),i,j)
    return val

def reveal(game, labels, rowOrCol, num): #shorthand for revealing entire row
    if rowOrCol == 'row':
        for j in range(0,5):
            revealElem(game, labels,num,j)
    elif rowOrCol == 'col':
        for i in range(0,5):
            revealElem(game, labels,i,num)

#Initial Row and Column Check
def charSumCheck(stats, labels): #check characteristic sum of
    charRow, charCol = newCharEq(labels, stats)
    print('Characteristic Sum of Rows: ' + str(charRow))
    for i, val in enumerate(charRow):
        cases = possibilities(val)
        print(cases)
        if cases == [(0, 0)]: #if there are no 2 or 3 tiles, eliminate that row
            labels.elim('row', i)
        if cases == [(1,0)]:#if there can only be a 2 tile in the row, mark it as such
            labels.updateRow('3', i)

    print('Characteristic Sum of Columns: ' + str(charCol))
    for i, val in enumerate(charCol):
        cases = possibilities(val)
        print(cases)
        if cases == [(0, 0)]: #if there are no 2 or 3 tiles, eliminate that column
            labels.elim('col', i)
        if cases == [(1, 0)]: #if there can only be a 2 tile in the column, mark it as such
            labels.updateCol('3',i)
    return charRow, charCol

def updateKnown(game,labels): #update known elements from game into labels
    for i in range(0,5):
        for j in range(0,5):
            if not game.map[i,j] == 'X':
                # print(game.map[i,j])
                labels.map[i,j] = game.map[i,j]

def mark(labels): #mark all '01' spaces with '-' for easier reading
    for i in range(0,5):
        for j in range(0,5):
            if labels.map[i,j] == '01':
                labels.map[i,j] = '-'