import cv2
import winsound
from cvzone.HandTrackingModule import HandDetector
from time import sleep
# pynput library allows you to control and monitor input devices.
from pynput.keyboard import Controller

# This will return video from the first webcam on your computer.
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set the width of the window.
cap.set(4, 720)  # Set the height of the window.


keyboard = Controller()
detector = HandDetector(detectionCon=0.8, maxHands=1)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]


def draw(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x+w, y+h), (25, 25, 112), cv2.FILLED)
        cv2.putText(img, button.text, (x+20, y+65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


def buttonLayout(color=(255, 0, 255)):
    cv2.rectangle(img, button.pos, (x + w, y + h), color, cv2.FILLED)
    cv2.putText(img, button.text, (x+20, y+65),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50 + i * 30, 100*i+50], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    img = draw(img, buttonList)

    if hands:
        hand1 = hands[0]
        lmList = hand1["lmList"]  # List of 21 Landmark points
        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                # Change color of key if index finger is in button.
                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    buttonLayout(color=(175, 0, 175))

                    # Calculate the distance between tip of index and middle finger.
                    length, info = detector.findDistance(lmList[8], lmList[12])

                    # If distance between index and middle finger is less than 40 then press the key.
                    if length < 40:
                        buttonLayout(color=(0, 255, 0))
                        keyboard.press(button.text)
                        # To generate a ‘Beep’ sound. winsound.Beep(Frquency, Milliseconds).
                        winsound.Beep(500, 100)
                        sleep(0.15)

    cv2.imshow("Image", img)

    # Press the ESC key, to exit
    if cv2.waitKey(1) == 27:
        break

# This releases the webcam, then closes all of the imshow() windows.
cap.release()  # Free memory
cv2.destroyAllWindows()
