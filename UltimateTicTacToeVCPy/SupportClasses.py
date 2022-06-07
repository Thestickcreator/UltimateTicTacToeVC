from numpy import reshape

class Game:
    tables = None # Matrice di tabelle
    paintedChecker = None # Finestra per mostrare lo stato attuale del gioco
    status = None
    turn = None
    def __init__(self, userBegins):
        self.tables = [[Table() for _ in range(3)] for _ in range(3)]
        self.status = [[0] * 3 for _ in range(3)]
        self.turn = userBegins # True = inizia lo user; False = inizia il computer
    def getTable(self, row, col):
        return self.tables[row][col].table
    def setTable(self, row, col, matrix):
        self.tables[row][col].table = matrix
    def setTableChecker(self, rowTable, colTable, rowC, colC, what):
        self.tables[rowTable][colTable].table[rowC][colC] = what # 1 = X; 2 = O; -1 = Gioco concluso; -2 = Pareggio
    def alreadyEnded(self, row, col):
        return self.status[row][col] > 0
    def tie(self, row, col):
        return self.status[row][col] == -2
    def updateWin(self, row, col, whoWon):
        self.status[row][col] = whoWon
    def updateTie(self, row, col):
        self.status[row][col] = -2

class Table:
    table = None
    def __init__(self):
        self.table = [[0] * 3 for _ in range(3)] # 0 = Casella vuota; 1 = X; 2 = O; -1 = Gioco concluso; -2 = Pareggio
    def resetEndedTable(self, whoWon):
        self.table = [[-1] * 3 for _ in range(3)]
        self.table[2][2] = whoWon
    def resetTiedTable(self):
        self.table = [[-2] * 3 for _ in range(3)]
    def checkWinTable(table): # Ritorna 0 = No Win; 1 = X Wins; 2 = O Wins
        # Per righe
        if table[0][0] == table[0][1] and table[0][0] == table[0][2] and table[0][0] in (1, 2): return table[0][0]
        if table[1][0] == table[1][1] and table[1][0] == table[1][2] and table[1][0] in (1, 2): return table[1][0]
        if table[2][0] == table[2][1] and table[2][0] == table[2][2] and table[2][0] in (1, 2): return table[2][0]
        # Per colonne
        if table[0][0] == table[1][0] and table[0][0] == table[2][0] and table[0][0] in (1, 2): return table[0][0]
        if table[0][1] == table[1][1] and table[0][1] == table[2][1] and table[0][1] in (1, 2): return table[0][1]
        if table[0][2] == table[1][2] and table[0][2] == table[2][2] and table[0][2] in (1, 2): return table[0][2]
        # Diagonali
        if table[0][0] == table[1][1] and table[0][0] == table[2][2] and table[0][0] in (1, 2): return table[0][0]
        if table[0][2] == table[1][1] and table[0][2] == table[2][0] and table[0][2] in (1, 2): return table[0][2]
        # No Wins
        return 0
    def checkTieTable(table): # Ritorna True o False
        if table[0][0] == -2: return True
        if table[0][0] == -1: return False
        return (0 not in reshape(table.copy(), 9)) and Table.checkWinTable(table) == 0
    def checkPlayableTable(table): # Table NON vinta né pareggiata
        if table[0][0] == -1 or table[0][0] == -2: return False
        return Table.checkWinTable(table) == 0 and (0 in reshape(table.copy(), 9))
