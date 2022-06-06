from CV import *
from SupportClasses import *
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
import math
from numpy import reshape
from numpy import argmax
from copy import deepcopy

# Implementazione di una generalizzazione dell'algoritmo Minimax
pruning = 5 # Vision per predict
pruningAdvanced1 = pruning+1
pruningAdvanced2 = pruning+2

# Valuta il Game in generale e attribuisce un punteggio allo stato corrente
def currentGeneralTableStatus(tables, currentTableIndexes, whoAmI):
    appEveluation = 0
    currentStatus = [[None, None, None], [None, None, None], [None, None, None]]
    weights = [[1.4, 1, 1.4], [1, 1.75, 1], [1.4, 1, 1.4]]
    for row in range(3):
        for col in range(3):
            appEveluation += howGoodIsThisTable(tables[row][col].table, whoAmI) * 1.5 * weights[row][col]
            if (row, col) == currentTableIndexes:
                appEveluation += howGoodIsThisTable(tables[row][col].table, whoAmI) * weights[row][col]
            tmpEv = Table.checkWinTable(tables[row][col].table)
            appEveluation -= tmpEv * weights[row][col]
            currentStatus[row][col] = tmpEv
    appEveluation -= Table.checkWinTable(currentStatus) * 5000 # Fine gioco, l'AI ha perso
    appEveluation += howGoodIsThisTable(currentStatus, whoAmI)*150 # Valutazione overall del game.status dal punto di vista dell'AI
    return appEveluation

# Metodi ausiliari
def symmetricalTable(table, whoAmI):
    tmp = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # 1 = Avversario (utente); -1 = IA
    for row in range(3):
        for col in range(3):
            if table[row][col] == 0: continue
            tmp[row][col] = (-1 if table[row][col] == whoAmI else 1)

    return tmp

def compareSumsOfAllRowsColsDiagonalsWithValue(table, x):
    return ((table[0][0] + table[0][1] + table[0][2] == x) or
       (table[1][0] + table[1][1] + table[1][2] == x) or
       (table[2][0] + table[2][1] + table[2][2] == x) or

       (table[0][0] + table[1][0] + table[2][0] == x) or
       (table[0][1] + table[1][1] + table[2][1] == x) or
       (table[0][2] + table[1][2] + table[2][2] == x) or

       (table[0][0] + table[1][1] + table[2][2] == x) or
       (table[0][2] + table[1][1] + table[2][0] == x))

def evaluateDoubles(table, not_full, full):
    app = 0
    # Posizionamenti doppi senza 3° checker
    # Righe
    if (table[0][0] + table[0][1] + table[0][2] == not_full or
        table[1][0] + table[1][1] + table[1][2] == not_full or
        table[2][0] + table[2][1] + table[2][2] == not_full):
        app += 6

    # Colonne
    if (table[0][0] + table[1][0] + table[2][0] == not_full or
        table[0][1] + table[1][1] + table[2][1] == not_full or
        table[0][2] + table[1][2] + table[2][2] == not_full):
        app += 6

    # Diagonali (hanno più peso)
    if(table[0][0] + table[1][1] + table[2][2] == not_full or
       table[0][2] + table[1][1] + table[2][0] == not_full):
        app += 7

    # Posizionamenti doppi con 3° checker avversario
    # Righe
    if ((table[0][0] + table[0][1] == 2 * full and table[0][2] == -full) or
        (table[0][1] + table[0][2] == 2 * full and table[0][0] == -full) or
        (table[0][0] + table[0][2] == 2 * full and table[0][1] == -full) or

        (table[1][0] + table[1][1] == 2 * full and table[1][2] == -full) or
        (table[1][0] + table[1][2] == 2 * full and table[1][1] == -full) or
        (table[1][1] + table[1][2] == 2 * full and table[1][0] == -full) or
        
        (table[2][0] + table[2][1] == 2 * full and table[2][2] == -full) or
        (table[2][1] + table[2][2] == 2 * full and table[2][0] == -full) or
        (table[2][0] + table[2][2] == 2 * full and table[2][1] == -full) or

    # Colonne
        (table[0][0] + table[1][0] == 2 * full and table[2][0] == -full) or
        (table[0][0] + table[2][0] == 2 * full and table[1][0] == -full) or
        (table[1][0] + table[2][0] == 2 * full and table[0][0] == -full) or

        (table[0][1] + table[1][1] == 2 * full and table[2][1] == -full) or
        (table[0][1] + table[2][1] == 2 * full and table[1][1] == -full) or
        (table[1][1] + table[2][1] == 2 * full and table[0][1] == -full) or
        
        (table[0][2] + table[1][2] == 2 * full and table[2][2] == -full) or
        (table[0][2] + table[2][2] == 2 * full and table[1][2] == -full) or
        (table[1][2] + table[2][2] == 2 * full and table[0][2] == -full) or
         
    # Diagonali
        (table[0][0] + table[1][1] == 2 * full and table[2][2] == -full) or
        (table[0][0] + table[2][2] == 2 * full and table[1][1] == -full) or
        (table[1][1] + table[2][2] == 2 * full and table[0][0] == -full) or

        (table[0][2] + table[1][1] == 2 * full and table[2][0] == -full) or
        (table[0][2] + table[2][0] == 2 * full and table[1][1] == -full) or
        (table[1][1] + table[2][0] == 2 * full and table[0][2] == -full)):
        app += 9

    return app

def howGoodIsThisTable(tableInAnalysis, whoAmI):
    evaluation = 0

    # Punteggio sommato/sottratto in base a: sub-gioco vinto
    possibleWin = Table.checkWinTable(tableInAnalysis)
    if possibleWin != 0: possibleWin = (-1 if possibleWin == whoAmI else 1)
    evaluation -= possibleWin * 12

    # Preparazione della table in analisi per essere valutata in modo simmetrico
    tableInAnalysis = symmetricalTable(tableInAnalysis, whoAmI)

    weights = [[0.2, 0.17, 0.2], [0.17, 0.22, 0.17], [0.2, 0.17, 0.2]]

    # Punteggio sommato/sottratto in base a: checker * peso
    for row in range(3):
        for col in range(3):
            evaluation -= tableInAnalysis[row][col] * weights[row][col];

    # Punteggio sommato/sottratto in base a: righe/colonne/diagonali riempite non interamente (full/not full)
    evaluation -= evaluateDoubles(tableInAnalysis, 2, -1)
    evaluation += evaluateDoubles(tableInAnalysis, -2, 1)

    return evaluation
    

# Una valutazione alta significa che si sta conquistando la Table
def howGoodIsThisMove(tableInAnalysis, currentCheckerIndexes, whoAmI):
    # Simulazione di una mossa
    appTableInAnalysis = deepcopy(tableInAnalysis)
    appTableInAnalysis[currentCheckerIndexes[0]][currentCheckerIndexes[1]] = whoAmI # Esecuzione mossa
    # Valutazione mossa
    evaluation = 0
    weights = [[0.2, 0.17, 0.2], [0.17, 0.22, 0.17], [0.2, 0.17, 0.2]] # Si preferiscono i posizionamenti al centro e ai bordi

    # Punteggio sommato/sottratto in base a: sub-gioco vinto
    possibleWin = Table.checkWinTable(appTableInAnalysis)
    if possibleWin != 0: possibleWin = (-1 if possibleWin == whoAmI else 1)
    evaluation -= possibleWin * 15
    
    # Preparazione della table in analisi per essere valutata in modo simmetrico
    appTableInAnalysis = symmetricalTable(appTableInAnalysis, whoAmI)
    
    evaluation += weights[currentCheckerIndexes[0]][currentCheckerIndexes[1]]

    # Punteggio sommato/sottratto in base a: creata una doppia
    doubleForAI = -2
    if compareSumsOfAllRowsColsDiagonalsWithValue(appTableInAnalysis, doubleForAI):
        evaluation += 1

    # Punteggio sommato/sottratto in base a: vittoria sub-gioco
    winForAI = -3
    if compareSumsOfAllRowsColsDiagonalsWithValue(appTableInAnalysis, winForAI):
        evaluation += 5

    # Punteggio sommato/sottratto in base a: "se l'avversario mettesse il suo checker lì, vincerebbe? E allora lo blocco"
    otherPlayer = (1 if whoAmI == 2 else 2)
    appTableInAnalysis[currentCheckerIndexes[0]][currentCheckerIndexes[1]] = otherPlayer

    winForOpponent = 3;
    if compareSumsOfAllRowsColsDiagonalsWithValue(appTableInAnalysis, winForOpponent):
        evaluation += 2

    return evaluation

# Algoritmo MiniMax - ricorsivo
def MiniMax(tables, currentTableIndexes, treeHeight, alpha, beta, turnInAnalysis, whoAmI):
    tmpPlay = None

    # Caso base
    currentEvaluation = currentGeneralTableStatus(tables, currentTableIndexes, whoAmI)
    if treeHeight <= 0 or abs(currentEvaluation) > 5000:
        return {"evaluation": currentEvaluation, "calculatedMove": None}

    # Caso ricorsivo
    # Analisi freeChoice a questa profondità dell'albero
    if currentTableIndexes == None: freeChoice = True
    else:
        freeChoice = False
        if(Table.checkWinTable(tables[currentTableIndexes[0]][currentTableIndexes[1]].table) != 0 or # Table conclusa
        Table.checkTieTable(tables[currentTableIndexes[0]][currentTableIndexes[1]].table)): # Table pareggiata
            freeChoice = True

    # Maximize
    if turnInAnalysis: # True = Maximize per l'utente; False = Minimize per l'AI
        maxEvaluationTillNow = -math.inf
        for row in range(3):
            for col in range(3):
                appEvaluation = -math.inf
                # freeChoice: analisi di tutte le Tables
                if freeChoice:
                    if Table.checkWinTable(tables[row][col].table) != 0: continue # La Table non deve essere conclusa
                    for rowTable in range(3):
                        for colTable in range(3):
    
                            if tables[row][col].table[rowTable][colTable] == 0: # Casella vuota
                                # Simulazione mossa: se l'AI effettua questa mossa, avviene la massimizzazione?
                                tables[row][col].table[rowTable][colTable] = whoAmI
                                appEvaluation = MiniMax(tables, (rowTable, colTable), treeHeight-1, alpha, beta, False, whoAmI)["evaluation"]
                                tables[row][col].table[rowTable][colTable] = 0
                            
                                # Valutazione mossa
                                if appEvaluation > maxEvaluationTillNow:
                                    maxEvaluationTillNow = appEvaluation
                                    tmpPlay = (row, col)

                                alpha = max(alpha, appEvaluation)

                    if beta <= alpha: break
                # non è in freeChoice: analisi della Table cardinata
                else:
                    if tables[currentTableIndexes[0]][currentTableIndexes[1]].table[row][col] == 0:
                        # Simulazione mossa
                        tables[currentTableIndexes[0]][currentTableIndexes[1]].table[row][col] = whoAmI
                        appEvaluation = MiniMax(tables, (row, col), treeHeight-1, alpha, beta, False, whoAmI)
                        tables[currentTableIndexes[0]][currentTableIndexes[1]].table[row][col] = 0

                        # Valutazione e salvataggio mossa
                        if appEvaluation["evaluation"] > maxEvaluationTillNow:
                            maxEvaluationTillNow = appEvaluation["evaluation"]
                            tmpPlay = appEvaluation["calculatedMove"]

                        alpha = max(alpha, appEvaluation["evaluation"])
                    if beta <= alpha: break

        return {"evaluation": maxEvaluationTillNow, "calculatedMove": tmpPlay}
    else: # Minimize
        otherPlayer = (1 if whoAmI == 2 else 2)
        minEvaluationTillNow = math.inf
        for row in range(3):            
            for col in range(3):                
                appEvaluation = math.inf
                # freeChoice: analisi di tutte le Tables
                if freeChoice:
                    if Table.checkWinTable(tables[row][col].table) != 0: continue # La Table non deve essere conclusa
                    for rowTable in range(3):
                        for colTable in range(3):
                            if tables[row][col].table[rowTable][colTable] == 0:
                                # Simulazione mossa: è meglio che l'avversario dell'AI effettui questa mossa? O ce ne sono altre che favoriscono ancora di più l'AI?
                                tables[row][col].table[rowTable][colTable] = otherPlayer
                                appEvaluation = MiniMax(tables, (rowTable, colTable), treeHeight-1, alpha, beta, True, whoAmI)["evaluation"]
                                tables[row][col].table[rowTable][colTable] = 0

                                # Valutazione e salvataggio mossa
                                if appEvaluation < minEvaluationTillNow:
                                    minEvaluationTillNow = appEvaluation
                                    tmpPlay = (rowTable, colTable)

                                beta = min(beta, appEvaluation)

                    if beta <= alpha: break
                # non è in freeChoice: analisi della Table cardinata
                else:
                    if tables[currentTableIndexes[0]][currentTableIndexes[1]].table[row][col] == 0:
                        tables[currentTableIndexes[0]][currentTableIndexes[1]].table[row][col] = otherPlayer
                        appEvaluation = MiniMax(tables, (row, col), treeHeight-1, alpha, beta, True, whoAmI)
                        tables[currentTableIndexes[0]][currentTableIndexes[1]].table[row][col] = 0

                        if appEvaluation["evaluation"] < minEvaluationTillNow:
                            minEvaluationTillNow = appEvaluation["evaluation"]
                            tmpPlay = appEvaluation["calculatedMove"]

                        beta = min(beta, appEvaluation["evaluation"])
                    if beta <= alpha: break
                       
        return {"evaluation": minEvaluationTillNow, "calculatedMove": tmpPlay}


# Metodi pubblici
def nextMove(game, freeChoice, currentTableIndexes, whoAmI, nMoves): # Codifica: ((rowTable, colTable), (row, col))
    # Preparazione bestMove e punteggi di ogni casella
    bestMove = None
    bestScore = [[-math.inf, -math.inf, -math.inf], [-math.inf, -math.inf, -math.inf], [-math.inf, -math.inf, -math.inf]] # Problema di ottimizzazione

    # Calcolo del numero di table ancora giocabili (utile nell'ambito del pruning)
    count = 0
    for row in range(3):
        for col in range(3):
            if not game.alreadyEnded(row, col) and not game.tie(row, col): count += 1

    #showinfo("Quanti liberi:", str(count)) #DEBUG
    #print(nMoves)
    if freeChoice:
        # freeChoice: Minimax per la scelta di quale table preferire
        if nMoves < 10: current_pruning = pruning
        elif 10 <= nMoves <= 15: current_pruning = pruningAdvanced1
        else: current_pruning = pruningAdvanced2
        savedMm = MiniMax(game.tables, None, min(current_pruning-1, count), -math.inf, math.inf, True, whoAmI)
        if savedMm["calculatedMove"] is not None: currentTableIndexes = savedMm["calculatedMove"]
        
    currentTable = game.getTable(currentTableIndexes[0], currentTableIndexes[1])
    #showinfo("Status:", game.tables[1][1].table) #DEBUG

    # Mossa random settata, verrà poi affinata
    for row in range(3):
        for col in range(3):
            if currentTable[row][col] == 0:
                bestMove = (row, col)
                break

    if bestMove is None: # Bug(?)
        showerror("Errore", "Si sta giocando in una Table piena. Partita conclusa.")
        exit()
        
    # Simulazioni di tutte le mosse possibili in questa Table (a livello locale ed allo "strato" attuale) con conseguente valutazione
    for row in range(3):
        for col in range(3):
            if currentTable[row][col] == 0:
                #showinfo("Status:", str(currentTable) + "  " + str(currentTableIndexes) + "  " + str(row) + "  " + str(col)) # DEBUG
                score = howGoodIsThisMove(currentTable, (row, col), whoAmI) * 45
                bestScore[row][col] = score

    # Applicazione di MiniMax e controllo predicts in profondità
    for row in range(3):
        for col in range(3):
            #if Table.checkWinTable(currentTable) == 0:
            if currentTable[row][col] == 0:
                # Simulazione mossa
                game.tables[currentTableIndexes[0]][currentTableIndexes[1]].table[row][col] = whoAmI
                if nMoves < 20: current_pruning = pruning
                elif 20 <= nMoves <= 30: current_pruning = pruningAdvanced1
                else: current_pruning = pruningAdvanced2
                predict = MiniMax(game.tables, (row, col), min(current_pruning, count), -math.inf, math.inf, False, whoAmI)
                game.tables[currentTableIndexes[0]][currentTableIndexes[1]].table[row][col] = 0

                bestScore[row][col] += predict["evaluation"]
    

    # Restituisce l'effettiva mossa migliore, sulla base del punteggio maggiore
    indexBM = argmax(reshape(bestScore, 9))
    bestMove = (int(indexBM / 3), indexBM % 3)

    return ((currentTableIndexes[0], currentTableIndexes[1]), (bestMove[0], bestMove[1]))
