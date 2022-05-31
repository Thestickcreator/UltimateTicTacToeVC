from CV import *
from SupportClasses import *
from tkinter.messagebox import showerror

# Metodi pubblici
def nextMove(game, freeChoice, currentTableIndexes, whoAmI): # Codifica: ((rowTable, colTable), (row, col))
    if freeChoice: # Scelta libera: inizio partita o table già conclusa
        return
    else: # Scelta cardinata
        return ((1,1), (2,2))
    return None
