import cv2
import numpy as np

#Global
LB = 0
UB = 0
Appr = 0.01
bgChecker = None
centerChecker = [0, 0, 0, 0]


def minn(x):
    global LB
    LB = cv2.getTrackbarPos("LivelloMin", "Sliders")
def maxx(x):
    global UB
    UB = cv2.getTrackbarPos("LivelloMax", "Sliders")
def approxx(x):
    global Appr
    Appr = cv2.getTrackbarPos("Approx", "Sliders")/1000 + 0.008


def drawWhatISeeWindow():
    cv2.namedWindow("What I see")
    global bgChecker
    bgChecker = np.zeros([512, 512, 1], np.uint8)
    bgChecker.fill(255)

    cv2.rectangle(bgChecker, (169, 64), (172, 470), (0, 0, 0), -1)
    cv2.rectangle(bgChecker, (328, 64), (331, 470), (0, 0, 0), -1)
    cv2.rectangle(bgChecker, (41, 193), (467, 196), (0, 0, 0), -1)
    cv2.rectangle(bgChecker, (41, 354), (467, 357), (0, 0, 0), -1)
    cv2.imshow("What I see", bgChecker)

def addCheckerToWindow(what, pos):
    global bgChecker
    center_coordinates = (120, 50)
    radius = 20

    # Line thickness of 2 px
    thickness = 2
    image = cv2.circle(bgChecker, center_coordinates, radius, (0, 0, 0), thickness)

    checker = None
    if what == 'C':
        checker = None

    if(pos == 'UL'):
        cv2.rectangle(bgChecker, (169, 64), (172, 470), (0, 0, 0), -1)

def main():
    global centerChecker
    cap = cv2.VideoCapture(0)

    bars = cv2.namedWindow("Sliders")
    cv2.createTrackbar("LivelloMin", "Sliders", 100, 255, minn) #38
    cv2.createTrackbar("LivelloMax", "Sliders", 255, 255, maxx) #108
    cv2.createTrackbar("Approx", "Sliders", 8, 100, approxx) #108

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

        for contour in contours:
            approx = cv2.approxPolyDP(contour, Appr * cv2.arcLength(contour, False), False)
            cv2.drawContours(frame, [approx], 0, (51, 252, 255), 3)
            rect = cv2.boundingRect(contour)
            if 21 <= len(approx) <= 23:
                #rect = cv2.boundingRect(contour)
                if rect[2] < 100 or rect[3] < 100: continue
                #print(cv2.contourArea(contour))
                x, y, w, h = rect
                refRect = rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

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
                cv2.putText(frame, "X " + str(len(approx)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            '''
            elif 4 <= len(approx) <= 40: # Trovare Checker O
                #rect = cv2.boundingRect(contour)
                x, y, w, h = rect
                cv2.putText(frame, "O " + str(len(approx)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            #elif: #Controlla le coordinate degli altri contour: se hanno x < quadrato nel mezzo
                #Allora raggruppali in una lista, poi tra loro confronta chi ha la y più alta
            '''

        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 120, param1=100, param2=30, minRadius=0, maxRadius=0)
        if circles is not None: # Trovare Checker O
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)

        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        drawWhatISeeWindow()

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

main()