import cv2
import numpy as np

class Game:
    tables = None # Matrice di tabelle
    paintedChecker = None # Finestra per mostrare lo stato attuale del gioco
    status = None
    def __init__(self):
        self.tables = [[Table() for _ in range(3)] for _ in range(3)]
        self.status = [[0] * 3 for _ in range(3)]
    def getTable(self, row, col):
        return self.tables[row][col].table
    def setTable(self, row, col, matrix):
        self.tables[row][col].table = matrix
    def checkWinGame(self): # Ritorna 0 = No Win; 1 = X Wins; 2 = O Wins
        for row in range(3):
            for col in range(3):
                self.status[row][col] = Table.checkWinTable(self.tables[row][col].table) # Vittoria registrata
                if self.status[row][col] != 0:
                    # Reset di quel sotto-gioco
                    self.tables[row][col].resetTable()
                    drawWinInWhatISeeWindow(self, row, col, self.status[row][col])
        #Check vittoria sulla matrice di stato
        return Table.checkWinTable(self.status)

class Table:
    table = None
    def __init__(self):
        self.table = [[0] * 3 for _ in range(3)] # 0 = Casella vuota; 1 = X; 2 = O; -1 = Gioco concluso
    def resetTable(self):
        self.table = [[-1] * 3 for _ in range(3)]
    def checkWinTable(table): # Ritorna 0 = No Win; 1 = X Wins; 2 = O Wins
        # Per righe
        if table[0][0] == table[0][1] and table[0][0] == table[0][2] and table[0][0] != 0: return table[0][0]
        if table[1][0] == table[1][1] and table[1][0] == table[1][2] and table[1][0] != 0: return table[1][0]
        if table[2][0] == table[2][1] and table[2][0] == table[2][2] and table[2][0] != 0: return table[2][0]
        # Per colonne
        if table[0][0] == table[1][0] and table[0][0] == table[2][0] and table[0][0] != 0: return table[0][0]
        if table[0][1] == table[1][1] and table[0][1] == table[2][1] and table[0][1] != 0: return table[0][1]
        if table[0][2] == table[1][2] and table[0][2] == table[2][2] and table[0][2] != 0: return table[0][2]
        # Diagonali
        if table[0][0] == table[1][1] and table[0][0] == table[2][2] and table[0][0] != 0: return table[0][0]
        if table[0][2] == table[1][1] and table[0][2] == table[2][0] and table[0][2] != 0: return table[0][2]
        # No Wins
        return 0
        
#Global
LB = 0
UB = 0
Appr = 0.01
colorX = (0, 252, 255)
colorO = (255, 0, 0)
colorNeutral = (43, 240, 96)

area_h = 256 # Altezza di una sola casella della macro tabella
area_w = 256 # Larghezza di una sola casella della macro tabella
offset = 20 # Spiazzamento rispetto ai bordi della finestra "What I See"

# Funzioni di appoggio per finestra "Sliders"
def minn(x):
    global LB
    LB = cv2.getTrackbarPos("LivelloMin", "Sliders")
def maxx(x):
    global UB
    UB = cv2.getTrackbarPos("LivelloMax", "Sliders")
def approxx(x):
    global Appr
    Appr = cv2.getTrackbarPos("Approx", "Sliders")/1000 + 0.008

# --------------------------------------------------------------------------------------------------------
# Grafica: Finestra "What I See"
# Metodi di appoggio

def init_bgWhatISee():
    happ = area_h * 3
    wapp = area_w * 3
    bgChecker = np.zeros([offset*2+happ, offset*2+wapp, 3], np.uint8)
    bgChecker.fill(255)

    cv2.rectangle(bgChecker, (area_w+offset, offset), (area_w+offset, happ+offset), colorNeutral, 2)
    cv2.rectangle(bgChecker, (area_w*2+offset, offset), (area_w*2+offset, happ+offset), colorNeutral, 2)
    cv2.rectangle(bgChecker, (offset, area_h+offset), (wapp+offset, area_h+offset), colorNeutral, 2)
    cv2.rectangle(bgChecker, (offset, area_h*2+offset), (wapp+offset, area_h*2+offset), colorNeutral, 2)
    # Disegna i sotto-giochi
    width_subarea = int((area_w-2*offset)/3)
    heigth_subarea = int((area_h-2*offset)/3)
    for vertical in range(3):
        for horizontal in range(3):
            offsetX = area_h*horizontal+offset
            offsetY = area_w*vertical+offset
            cv2.rectangle(bgChecker, (offsetX+width_subarea+offset, offsetY+offset), (offsetX+width_subarea+offset, offsetY+(heigth_subarea*3)+offset), (0, 0, 0), -1)
            cv2.rectangle(bgChecker, (offsetX+width_subarea*2+offset, offsetY+offset), (offsetX+width_subarea*2+offset, offsetY+(heigth_subarea*3)+offset), (0, 0, 0), -1)
            cv2.rectangle(bgChecker, (offsetX+offset, offsetY+width_subarea+offset), (offsetX+(width_subarea*3)+offset, offsetY+width_subarea+offset), (0, 0, 0), -1)
            cv2.rectangle(bgChecker, (offsetX+offset, offsetY+heigth_subarea*2+offset), (offsetX+(width_subarea*3)+offset, offsetY+heigth_subarea*2+offset), (0, 0, 0), -1)
    return bgChecker
   
def drawX(game, pos):
    # Disegna 2 linee
    length_of_line = ((area_w-2*offset)/3) * 0.8 # = dimensione subarea con un rapporto dell'80%
    starting_point = int((length_of_line/2)*np.cos(np.pi/4))
    cv2.line(game.paintedChecker, (pos[0]-starting_point, pos[1]-starting_point), (pos[0]+starting_point, pos[1]+starting_point), colorX, thickness=2)
    cv2.line(game.paintedChecker, (pos[0]+starting_point, pos[1]-starting_point), (pos[0]-starting_point, pos[1]+starting_point), colorX, thickness=2)

def drawO(game, pos):
    radius = int((((area_w-2*offset)/3)/2) * (0.8)) # Raggio = dimensione subarea/2 con un rapporto dell'80%
    cv2.circle(game.paintedChecker, (pos[0], pos[1]), radius, colorO, 2) # Spessore = 1
    
def drawWinInWhatISeeWindow(game, row, col, who):
    cv2.rectangle(game.paintedChecker,
                          (2*offset+area_w*col, 2*offset+area_h*row), 
                          (area_w*col+area_w, area_h*row+area_h), (255, 255, 255), -1)
    if who == 1: # X Wins
        # Disegna 2 linee
        length_of_line = (area_w-2*offset) * 0.8 # = dimensione area/2 con un rapporto dell'80%
        starting_point = int((length_of_line/2)*np.cos(np.pi/4))
        offsetX = int(area_w*col+area_w/2)
        offsetY = int(area_h*row+area_h/2)
        cv2.line(game.paintedChecker, (offsetX-starting_point+offset, offsetY-starting_point+offset), (offsetX+starting_point+offset, offsetY+starting_point+offset), colorX, thickness=3)
        cv2.line(game.paintedChecker, (offsetX+starting_point+offset, offsetY-starting_point+offset), (offsetX-starting_point+offset, offsetY+starting_point+offset), colorX, thickness=3)
    else: # O Wins
        radius = int(((area_w-2*offset)/2) * (0.8)) # Raggio = dimensione area/2 con un rapporto dell'80%
        cv2.circle(game.paintedChecker, (area_w*col+int(area_w/2)+offset, area_h*row+int(area_h/2)+offset), radius, colorO, 3) # Spessore = 3  
    cv2.imshow("What I see", game.paintedChecker)
    
# Metodi pubblici -------------------------------------------------
def showWhatISeeWindow(game):
    cv2.namedWindow("What I see")
    game.paintedChecker = init_bgWhatISee()
    cv2.imshow("What I see", game.paintedChecker)
                
def drawTableOnbgWhatISee(game, table, offsetX, offsetY):
    w_subarea = (area_w-2*offset)/3
    h_subarea = (area_h-2*offset)/3
    trait_w = int(w_subarea/2)
    trait_h = int(h_subarea/2)
    posMatrix = [[(trait_w, trait_h), (3*trait_w, trait_h), (5*trait_w, trait_h)],
                 [(trait_w, 3*trait_h), (3*trait_w, 3*trait_h), (5*trait_w, 3*trait_h)],
                 [(trait_w, 5*trait_h), (3*trait_w, 5*trait_h), (5*trait_w, 5*trait_h)]]
    for row in range(3):
        for col in range(3):
            pos = (posMatrix[row][col][0] + offsetX + 2*offset, posMatrix[row][col][1] + offsetY + 2*offset)
            what = table[row][col]
            if what == 1: # Disegna X
                drawX(game, pos)
            elif what == 2: # Disegna O
                drawO(game, pos)  
    cv2.imshow("What I see", game.paintedChecker)

def updateWhatISeeWindow(game):    
    for gameRow in range(3):
        for gameCol in range(3):
            # Disegna X se checker[gameRow][gameCol] == 1. Oppure disegna O se checker[gameRow][gameCol] == 2
            drawTableOnbgWhatISee(game,
                                  game.getTable(gameRow, gameCol),
                                  gameCol * area_w, gameRow * area_h)
    cv2.imshow("What I see", game.paintedChecker)

def highlightCurrentTableInWhatISeeWindow(game, row, col):
    w = int(area_w/2-offset/2)
    h = int(area_h/2-offset/2)
    centerW = int(area_w/2)
    centerH = int(area_h/2)
    for rowApp in range(3):
        for colApp in range(3):
            cv2.rectangle(game.paintedChecker,
                          (centerW+offset-w+area_w*colApp, centerH+offset-h+area_h*rowApp),
                          (centerW+offset+w+area_w*colApp, centerH+offset+h+area_h*rowApp), (255, 255, 255), 2)
    cv2.rectangle(game.paintedChecker,
                          (centerW+offset-w+area_w*col, centerH+offset-h+area_h*row),
                          (centerW+offset+w+area_w*col, centerH+offset+h+area_h*row), (0, 0, 255), 2)
    cv2.imshow("What I see", game.paintedChecker)        

# --------------------------------------------------------------------------------------------------------
# CV
# Metodi di appoggio

def adjustPositions(listOfContours): # Creazione matrice 3x3 con le posizioni corrette
    #TODO
    return None

def checkAndSub(correctContours): # Controllo sovrapposizioni: restituisce una lista di 9 contours
    #TODO
    return None

# Metodi pubblici -------------------------------------------------
def scanTable(game, row, col, cap):
    while True:
        _, frame = cap.read()

        mask_min = np.array([LB, LB, LB])
        mask_max = np.array([UB, UB, UB])

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        mask = cv2.threshold(blurred, LB, UB, cv2.THRESH_BINARY_INV)[1]

        #CONTOURS

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        refRect = None
        refCentral = None
        currentContous = {}
        currentContous["checkers"] = []

        for contour in contours:
            approx = cv2.approxPolyDP(contour, Appr * cv2.arcLength(contour, False), False)
            rect = cv2.boundingRect(contour)
            if 21 <= len(approx) <= 23:
                #rect = cv2.boundingRect(contour)
                if rect[2] < 100 or rect[3] < 100: continue
                x, y, w, h = rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.drawContours(frame, [approx], 0, (43, 240, 96), 3) # Disegna il contour rilevato per l'area di gioco

                cv2.putText(frame, "Area di gioco", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                currentContous["ADG"] = (approx, rect)
                '''
                elif 5 <= len(approx) <= 10: # Riquadro al centro
                    #rect = cv2.boundingRect(contour)
                    a, b, c, d = rect
                    if "ADG" in currentContous:
                        x, y, w, h = currentContous["ADG"][1]
                        if x < a < (x+w) and y < b < (y+h) and x < (a+c) < (x+w) and y < (b+d) < (y+h): # Found
                            refCentral = rect
                            centerChecker[0] = (a, b)
                            centerChecker[1] = (a + c, b)
                            centerChecker[2] = (a, b + d)
                            centerChecker[3] = (a + c, b + d)
                            #cv2.rectangle(frame, (a, b), (a + c, b + d), (0, 255, 0), 2)
                            cv2.putText(frame, str(len(approx)), (a, b), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            currentContous["checkers"].append((approx, rect))
                '''
            elif 12 <= len(approx) <= 18: # Trovare Checker X
                rect = cv2.boundingRect(contour)
                x, y, w, h = rect
                # Se è rilevata una X, allora PROBABILMENTE è corretta. Rimane da constatare se si trova all'interno dell'area di gioco o meno
                if "ADG" in currentContous:
                    x_ADG, y_ADG, w_ADG, h_ADG = currentContous["ADG"][1]
                    if x_ADG < x < (x_ADG+w_ADG) and y_ADG < y < (y_ADG+h_ADG): # Trovata possibile X interna all'area di gioco
                        currentContous["checkers"].append((1, approx, rect))
                        cv2.putText(frame, "X", (int(x+w/2), int(y+h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colorX, 2) # Disegna X in giallo

        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 120, param1=100, param2=30, minRadius=0, maxRadius=0)
        if circles is not None: # Trovare Checker O
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # Se è rilevato un O, allora è SICURAMENTE corretto. Rimane da constatare se si trova all'interno dell'area di gioco o meno
                if "ADG" in currentContous:
                    x_ADG, y_ADG, w_ADG, h_ADG = currentContous["ADG"][1]
                    if x_ADG < i[0] < (x_ADG+w_ADG) and y_ADG < i[1] < (y_ADG+h_ADG): # Trovato O interno all'area di gioco
                        currentContous["checkers"].append((2, i, (i[0], i[1])))
                        cv2.circle(frame, (i[0], i[1]), i[2], colorO, 3) # Disegna O in blu


        drawTableOnbgWhatISee(game, game.getTable(row, col), col * area_w, row * area_h)
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        key = cv2.waitKey(1)
        if key == 27: # Interrompi scansione con il tasto "ESC"
            # Rileva eventuali sovrapposizioni con altri contour già presenti - in caso, sostituisci eventuali X erroneamente rilevate
            correctContours = checkAndSub(currentContours)
            # Rileva posizione rispetto a centerChecker e modifica checker (la variabile globale)
            return adjustPositions(correctContours)

# Main
def main():
    game = Game()
    
    cap = cv2.VideoCapture(0)

    bars = cv2.namedWindow("Sliders")
    cv2.createTrackbar("LivelloMin", "Sliders", 100, 255, minn) #38
    cv2.createTrackbar("LivelloMax", "Sliders", 255, 255, maxx) #108
    cv2.createTrackbar("Approx", "Sliders", 8, 100, approxx) #108

    showWhatISeeWindow(game)
    game.getTable(0, 1)[0][0] = 1
    game.getTable(0, 1)[0][1] = 1
    game.getTable(0, 1)[0][2] = 1
    game.getTable(1, 1)[0][0] = 2
    updateWhatISeeWindow(game)
    highlightCurrentTableInWhatISeeWindow(game, 1, 1)
    
    drawWinInWhatISeeWindow(game, 1, 2, 2)
    drawWinInWhatISeeWindow(game, 2, 2, 1)
    drawWinInWhatISeeWindow(game, 1, 1, 1)
    game.checkWinGame()
    
    game.setTable(1, 1, scanTable(game, 1, 1, cap))
    updateWhatISeeWindow(game)       
    
    cap.release()
    cv2.destroyAllWindows()

main()
