import cv2
import numpy as np
LB = 0
UB = 0


def minn(x):
    global LB
    LB = cv2.getTrackbarPos("LivelloMin", "Sliders")
def maxx(x):
    global UB
    UB = cv2.getTrackbarPos("LivelloMax", "Sliders")

cap = cv2.VideoCapture(0)

bars = cv2.namedWindow("Sliders")
cv2.createTrackbar("LivelloMin", "Sliders", 38, 255, minn) #38
cv2.createTrackbar("LivelloMax", "Sliders", 108, 255, maxx) #108

while True:
    _, frame = cap.read()

    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    mask_min = np.array([LB, LB, LB])
    mask_max = np.array([UB, UB, UB])
    mask = cv2.inRange(frame, mask_min, mask_max)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, )

    #CONTRAST
    alpha = 2  # Contrast control (1.0-3.0)
    beta = 0  # Brightness control (0-100)

    mask = cv2.convertScaleAbs(mask, alpha=alpha, beta=beta)

    #CONTOURS
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, False), False)
        cv2.drawContours(frame, [approx], 0, (51, 252, 255), 3)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()