import cv2
import numpy as np

class Game:
    tables = None # Matrice di tabelle
    paintedChecker = None # Finestra per mostrare lo stato attuale del gioco
    def __init__(self):
        self.tables = [[Table() for _ in range(3)] for _ in range(3)]
    def getTable(self, row, col):
        return self.tables[row][col]
    def checkWinGame(self): # Ritorna 0 = No Win; 1 = X Wins; 2 = O Wins
        tmp = [[0] * 3] * 3
        for row in range(3):
            for col in range(3):
                tmp[row][col] = Table.checkWinTable(self.tables[row][col].table)
        #Check vittoria sulla matrice d'appoggio tmp
        return Table.checkWinTable(tmp)

class Table:
    table = None
    def __init__(self):
        self.table = [[0] * 3] * 3 # 0 = Casella vuota; 1 = X; 2 = O
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
centerChecker = [0, 0, 0, 0]

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

# Finestra "What I See"
def init_bgWhatISee():
    happ = area_h * 3
    wapp = area_w * 3
    bgChecker = np.zeros([offset*2+happ, offset*2+wapp, 3], np.uint8)
    bgChecker.fill(255)

    cv2.rectangle(bgChecker, (area_w+offset, offset), (area_w+offset, happ+offset), (43, 240, 96), 2)
    cv2.rectangle(bgChecker, (area_w*2+offset, offset), (area_w*2+offset, happ+offset), (43, 240, 96), 2)
    cv2.rectangle(bgChecker, (offset, area_h+offset), (wapp+offset, area_h+offset), (43, 240, 96), 2)
    cv2.rectangle(bgChecker, (offset, area_h*2+offset), (wapp+offset, area_h*2+offset), (43, 240, 96), 2)
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
   
def drawX(bg, pos):
    # Disegna 2 linee

def drawO(bg, pos):
    radius = int((((area_w-2*offset)/3)/2) * (0.8)) # Raggio = dimensione subarea/2 con un rapporto dell'80%
    cv2.circle(bg, (pos[0], pos[1]), radius, (255, 0, 0), 1) # Spessore = 1
            
def drawTableOnbgWhatISee(bg, table, offsetX, offsetY):
    #TODO: rendere funzionante drawTableOnbgWhatISee
    posMatrix = [[(100, 200), (300, 400), (500, 600)],
                 [(700, 800), (900, 1000), (1100, 1200)],
                 [(1300, 1400), (150, 1600), (1700, 1800)]]
    pos = (posMatrix[row][col][0] + offsetX, posMatrix[row][col][1] + offsetY)
    if what == 1: # Disegna X
        drawX(bg, pos)
    elif what == 2: # Disegna O
        drawO(bg, pos)
    
# Metodi "pubblici"
def showWhatISeeWindow(game):
    cv2.namedWindow("What I see")
    game.paintedChecker = init_bgWhatISee()
    cv2.imshow("What I see", game.paintedChecker)

def updateWhatISeeWindow(game):    
    for gameRow in range(3):
        for gameCol in range(3):
            # Disegna X se checker[gameRow][gameCol] == 1. Oppure disegna O se checker[gameRow][gameCol] == 2
            drawTableOnbgWhatISee(game.paintedChecker,
                                  game.tables[gameRow][gameCol],
                                  gameRow * 512, gameCol * 512)

#TODO Implementa checkAndSub
def checkAndSub(listC):
    return None

def main():
    global centerChecker
    game = Game()
    cap = cv2.VideoCapture(0)

    bars = cv2.namedWindow("Sliders")
    cv2.createTrackbar("LivelloMin", "Sliders", 100, 255, minn) #38
    cv2.createTrackbar("LivelloMax", "Sliders", 255, 255, maxx) #108
    cv2.createTrackbar("Approx", "Sliders", 8, 100, approxx) #108

    showWhatISeeWindow(game)
    updateWhatISeeWindow(game)
    
    return

    while True:
        _, frame = cap.read()

        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        mask_min = np.array([LB, LB, LB])
        mask_max = np.array([UB, UB, UB])

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        #thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
        mask = cv2.threshold(blurred, LB, UB, cv2.THRESH_BINARY_INV)[1]

        #mask = cv2.inRange(thresh, mask_min, mask_max)
        #kernel = np.ones((5, 5), np.uint8)
        #mask = cv2.erode(mask, kernel, )

        #CONTRAST
        #alpha = 2  # Contrast control (1.0-3.0)
        #beta = 0  # Brightness control (0-100)

        #mask = cv2.convertScaleAbs(mask, alpha=alpha, beta=beta)


        #CONTOURS

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        refRect = None
        refCentral = None
        correctContours = []

        for contour in contours:
            approx = cv2.approxPolyDP(contour, Appr * cv2.arcLength(contour, False), False)
            rect = cv2.boundingRect(contour)
            if 21 <= len(approx) <= 23:
                #rect = cv2.boundingRect(contour)
                if rect[2] < 100 or rect[3] < 100: continue
                #print(cv2.contourArea(contour))
                x, y, w, h = rect
                refRect = rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.drawContours(frame, [approx], 0, (51, 252, 255), 3) # Disegna il contour rilevato per l'area di gioco


                #M = cv2.moments(contour)
                #cX = int(M["m10"] / M["m00"])
                #cY = int(M["m01"] / M["m00"])
                cv2.putText(frame, "Area di gioco", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            elif 5 <= len(approx) <= 10: # Riquadro al centro
                #rect = cv2.boundingRect(contour)
                a, b, c, d = rect
                if refRect is not None:
                    x, y, w, h = refRect
                    if x < a < (x+w) and y < b < (y+h) and x < (a+c) < (x+w) and y < (b+d) < (y+h): # Found
                        refCentral = rect
                        centerChecker[0] = (a, b)
                        centerChecker[1] = (a + c, b)
                        centerChecker[2] = (a, b + d)
                        centerChecker[3] = (a + c, b + d)
                        #cv2.rectangle(frame, (a, b), (a + c, b + d), (0, 255, 0), 2)
                        cv2.putText(frame, str(len(approx)), (a, b), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            elif 12 <= len(approx) <= 18: # Trovare Checker X
                #rect = cv2.boundingRect(contour)
                x, y, w, h = rect
                # Se è rilevata una X, allora PROBABILMENTE è corretta
                cv2.putText(frame, "X " + str(len(approx)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                # Rileva posizione rispetto a centerChecker e aggiungi alla lista dei checker a sinsitra, destra o centro
                #TODO Implementa i 3 gruppi sinitra, destra e tra i 2 quello al centro
                #Fai sort tra loro confronta chi ha la y più alta e fai sort a 
            '''
            elif 4 <= len(approx) <= 40: # Trovare Checker O
                #rect = cv2.boundingRect(contour)
                x, y, w, h = rect
                cv2.putText(frame, "O " + str(len(approx)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            #elif: #Controlla le coordinate degli altri contour: se hanno x < quadrato nel mezzo
                
            '''

        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 120, param1=100, param2=30, minRadius=0, maxRadius=0)
        if circles is not None: # Trovare Checker O
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:

                correctContours.append((i, 2)) # Se è rilevato un O, allora è sicuramente corretto
                # Controlla se è dentro l'area di gioco stile if x < a < (x+w) and y < b < (y+h) and x < (a+c) < (x+w) and y < (b+d) < (y+h):
                # Rileva eventuali sovrapposizioni con altri contour già presenti - in caso, sostituisci eventuali X erroneamente rilevate
                checkAndSub(correctContours)
                # Rileva posizione rispetto a centerChecker e modifica checker (la variabile globale)

        # Disegna i contour rilevati correttamente come X o O
        for item in correctContours:
            if item[1] == 1:
                cv2.drawContours(frame, [item], 0, (51, 252, 255), 3) # Disegna le X in giallo
            elif item[1] == 2:
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 0, 255), 3) # Disegna i O in blu


        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        drawWhatISeeWindow()

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

main()
