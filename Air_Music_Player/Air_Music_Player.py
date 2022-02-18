import cv2
import cvzone
import random
from pygame import mixer
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
mixer.init()

animationpng = cv2.imread("Images\\stars1.png", cv2.IMREAD_UNCHANGED)
animationpng = cv2.resize(animationpng, (1280, 720))


def drawrectangle(img, x, y, color):
    '''This function draw the rectange at the tip of all fingers.'''

    w, h = 15, 15
    cv2.rectangle(img, (x-w, y-h), (x + w, y + h), color, cv2.FILLED)


def calulateDistance():
    ''' This Function calculate the distance betneew the startpoint and endpoint lmlist distance of the fingers '''

    # List of fingers
    fingers = ['index', 'middle', 'ring', 'little', 'thumb']
    startpoints = [8, 12, 16, 20, 4]  # lmList points of the fingers.
    endpoints = [5, 9, 13, 17, 5]  # lmList points of the fingers.

    # List to store the distance between repective startpoints and endpoints
    fingersdist = []
    for st, en in zip(startpoints, endpoints):
        dist, _ = detector.findDistance(lmlist[st], lmlist[en])
        fingersdist.append(dist)

    # return dictionary : fingers as key and fingesrdist as a value.
    return dict(zip(fingers, fingersdist))


def musicplay(fingerdictic, img):
    '''This function play the music and overlay the PNG image when lmlist distance of fingers is less than some threshold.'''

    if fingerdict['index'] < 20:
        mixer.Sound("sounds\Piano_C.wav").play()
        img = cvzone.overlayPNG(img, animationpng)

    if fingerdict['middle'] < 20:
        mixer.Sound("sounds\Piano_D.wav").play()
        img = cvzone.overlayPNG(img, animationpng)

    if fingerdict['ring'] < 20:
        mixer.Sound("sounds\Piano_E.wav").play()
        img = cvzone.overlayPNG(img, animationpng)

    if fingerdict['little'] < 20:
        mixer.Sound("sounds\Piano_F.wav").play()
        img = cvzone.overlayPNG(img, animationpng)

    if fingerdict['thumb'] < 20:
        mixer.Sound("sounds\Piano_G.wav").play()
        img = cvzone.overlayPNG(img, animationpng)

    return img


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands = detector.findHands(img, draw=False)

    if hands:
        hand1 = hands[0]
        lmlist = hand1["lmList"]  # List of 21 Landmark points

        # Draw rectangle over all the five fingers.
        fingerslist = [8, 12, 16, 20, 4]  # lmlist points for the fingers.
        colors = [(0, 255, 255), (255, 0, 0), (0, 255, 0),
                  (0, 0, 255), (25, 25, 112)]
        for f, c in zip(fingerslist, colors):
            drawrectangle(img, lmlist[f][0], lmlist[f][1], color=c)

        # call calculateDistnace function to calculate distance between lmlist points
        fingerdict = calulateDistance()

        # call musicplay function to play music based on distance between lmlist points.
        img = musicplay(fingerdict, img)

    cv2.imshow("Image", img)

    # Press the ESC key, to exit
    if cv2.waitKey(1) == 27:
        break


# This releases the webcam, then closes all of the imshow() windows.
cap.release()  # Free memory
cv2.destroyAllWindows()
