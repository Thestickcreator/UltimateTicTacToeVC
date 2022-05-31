import cv2
import numpy as np
from CV import *
from IA import *
from SupportClasses import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import askyesno
from tkinter.messagebox import showinfo
from random import randint

# Variabili globali
ROOT = None

# Metodi ausiliari
def checkWinGame(game): # Ritorna 0 = No Win; 1 = X Wins; 2 = O Wins
    for row in range(3):
        for col in range(3):
            game.status[row][col] = Table.checkWinTable(game.tables[row][col].table) # Vittoria registrata
            if game.status[row][col] != 0:
                # Reset di quel sotto-gioco
                game.tables[row][col].resetTable()
                drawWinInWhatISeeWindow(game, row, col, game.status[row][col]) # Update grafico
    # Check vittoria sulla matrice di stato
    return Table.checkWinTable(game.status)

def whatsTheLastMove(before, after):
    listOfDifferences = []
    for row in range(3):
        for col in range(3):
            if before[row][col] != after[row][col]: listOfDifferences.append(((row, col), after[row][col]))
    if len(listOfDifferences) != 1:
        ROOT = tk.Tk()
        ROOT.withdraw()
        showerror("End", "Rilevate molteplici mosse. Partita conclusa.")
        exit()
    return listOfDifferences[0]

# Play
def play(game):
    # game.turn: True = Turno dello user; False = Turno del computer
    freeChoice = True # Scelta libera per user o computer. Accade all'inizio o quando si dovrebbe giocare in una table già conclusa
    currentTableIndexes = None
    currentChecker = True # True = X; False = O
    previousArrangement = None # Copia di appoggio del precedente arrangement della table da scansionare
    
    while True:
        whatChecker = (1 if currentChecker else 2)
        if game.turn:
            # Turno dello user
            if freeChoice: # Scelta libera: inizio partita o table già conclusa
                while True:                    
                    inputUsr = askstring("Selezione Table da scansionare", "Inserisci una qualsiasi tabella da scansionare nella forma <row,column>")
                    if inputUsr is not None and len(inputUsr) == 3:
                        inputUsr = inputUsr.split(",")
                        # Check se quella table è già conclusa
                        tableToScan = (int(inputUsr[0]), int(inputUsr[1]))
                        if tableToScan[0] not in (0,1,2) or tableToScan[1] not in (0,1,2):
                            showerror("Errore", "Indici non corretti! Riprovare l'inserimento.")
                        else:
                            if not game.alreadyEnded(tableToScan[0], tableToScan[1]): break
                            else: showerror("Errore", "La table scelta è già conclusa! Riprovare l'inserimento.")
                    else: showerror("Errore", "Errore nell'inserimento! Riprovare.")
                toScanIndexes = tableToScan
            else: # Scelta cardinata
                toScanIndexes = currentTableIndexes
                
            highlightCurrentTableInWhatISeeWindow(game, toScanIndexes[0], toScanIndexes[1]) # Aggiorna focus
            previousArrangement = game.getTable(toScanIndexes[0], toScanIndexes[1]).copy()
            scanTable(game, toScanIndexes[0], toScanIndexes[1])                       
            currentTableIndexes = whatsTheLastMove(previousArrangement, game.getTable(toScanIndexes[0], toScanIndexes[1]))
            
            if currentTableIndexes[1] != whatChecker:
                whatChecker = ("X" if currentChecker else "O")
                scannedChecker = ("X" if currentTableIndexes[1]==1 else "O")
                showerror("End", "Inserito checker (" + scannedChecker + ") diverso da quello atteso (" + whatChecker + "). Partita conclusa.")
                exit()
            currentTableIndexes = currentTableIndexes[0]
            #print(currentTableIndexes)
            freeChoice = (False if not game.alreadyEnded(currentTableIndexes[0], currentTableIndexes[1]) else True) 
        else:
            # Turno del computer            
            nM = nextMove(game, freeChoice, currentTableIndexes, whatChecker) # Codifica: ((rowTable, colTable), (row, col))
            game.setTableChecker(nM[0][0], nM[0][1], nM[1][0], nM[1][1], whatChecker)
            updateWhatISeeWindow(game)
            currentTableIndexes = (nM[1][0], nM[1][1])
            freeChoice = (False if not game.alreadyEnded(nM[1][0], nM[1][1]) else True)
            
        cW = checkWinGame(game) # Controllo eventuale vittoria ad ogni mossa
        if cW != 0:
            break
        
        game.turn = not game.turn # Cambio turno
        currentChecker = not currentChecker # La prossima mossa sarà con l'altro checker
        
    whoWins = ("lo user" if game.turn else "il computer") # Ha vinto il giocatore che ha eseguito l'ultima mossa
    showinfo("Fine gioco", "Ha vinto " + whoWins + " con i checker " + ("X" if cW == 1 else "O") + "!")
            
# Main
def main():
    
    # Chi inizia?
    ROOT = tk.Tk()
    ROOT.withdraw()
    coinFlip = askyesno("Testa o croce", "Scegli testa?")
    coinFlip = (1 if coinFlip else 2) # 1 = Testa; 2 = Croce
    outcome = randint(1, 2)
    video = cv2.VideoCapture("Testa.mp4" if outcome == 1 else "Croce.mp4")
    while(video.isOpened()):
        ret, frame = video.read()
        if ret:
            cv2.imshow("Testa o Croce", frame)
            cv2.waitKey(17)
        else:
            break
    
    userBegins = (True if outcome == coinFlip else False) # Si comincia sempre con X. True = inizia lo user; False = inizia il computer  

    # Nuovo gioco
    uttt = Game(userBegins)

    whoBegins = ("lo user" if uttt.turn else "il computer")
    showinfo("Inizio gioco", "È uscito " + ("testa" if outcome == 1 else "croce") + ", quindi comincia " + whoBegins + " con i checker X!") 

    # Release delle finestre per il testa o croce
    video.release()
    cv2.destroyAllWindows()
    
    showWhatISeeWindow(uttt)
    #updateWhatISeeWindow(uttt)
    #highlightCurrentTableInWhatISeeWindow(uttt, 1, 1)
    
    #scanTable(uttt, 1, 1)
    #checkWinGame(uttt)
    play(uttt)
    
    cv2.destroyAllWindows()

main()
