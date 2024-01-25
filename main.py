import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1288)  # prop-id for width is 3 , so width = 1288
cap.set(4, 720)  # prop-id for height is 4, so height = 720

# detection confidence probability
detector = HandDetector(detectionCon=0.8, maxHands=1)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "-"]]

finalText = ""

keyboard = Controller()

# without transparency


def drawALL(img, buttonList):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x+w, y+h), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, button.text, (x+20, y+65),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    return img


# with tranceparency
# def drawALL(img, buttonList):
#     imgNew = np.zeros_like(img, np.uint8)
#     for button in buttonList:
#         x, y = button.pos
#         cvzone.cornerRect(
#             imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
#         cv2.rectangle(imgNew, button.pos, (x + button.size[0],  y + button.size[1]),
#                       (255, 0, 255), cv2.FILLED)
#         cv2.putText(imgNew, button.text, (x + 40, y + 60),
#                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
#
#     out = img.copy()
#     alpha = 0.05
#     mask = imgNew.astype(bool)
#     print(mask.shape)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1-alpha, 0)[mask]
#     return out


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50, 100*i+50], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)
    img = drawALL(img, buttonList)

    if hands:
        hand1 = hands[0]

        lmList = hand1["lmList"]

        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][0] < x+w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x+w, y+h),
                                  (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x+20, y+65),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

                    # l, _, img = detector.findDistance(
                    #     lmList[8][1], lmList[12][0], img)
                    # print(l)
                    # l, _, img = detector.findDistance(
                    #     hand1[8], hand1[12], img)
                    # print(l)

                    l, _, img = detector.findDistance(
                        lmList[8][:2], lmList[12][:2], img)
                    print(l)

                    if l < 50:

                        keyboard.press(button.text)

                        cv2.rectangle(img, button.pos, (x+w, y+h),
                                      (175, 0, 175), cv2.FILLED)
                        cv2.putText(img, button.text, (x+20, y+65),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

                        if button.text == "-" and len(finalText) != 0:
                            finalText = finalText[:-1]
                            keyboard.press('\b')
                            sleep(0.5)
                        else:
                            finalText += button.text
                            sleep(0.5)

    cv2.rectangle(img, (50, 350), (700, 450),
                  (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


# with draw , using flipType = False we can have left hand as right and vice versa
    # hands, img = detector.findHands(img, draw=False)  # no draw

    # in cvzone version 1.5+  'hand' is a list has info about lmList , bbox in a dict etc
    # Hand - dict_(lmList - bbox - center - type)   ~info like this for every hand
    # lmList, bboxInfo = detector.findPosition(img)


# Used this is the class button since we need multiple buttons for the keyboard
    # # for the button (img, location , size , color , type)
    # cv2.rectangle(img, (100, 100), (200, 200), (255, 0, 255), cv2.FILLED)
    # cv2.putText(img, "Q", (120, 170), cv2.FONT_HERSHEY_PLAIN,
    #             5, (255, 255, 255), 5)  # for the alphabet in the button(img , text , location , font , height , color ,width )
