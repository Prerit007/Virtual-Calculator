import cv2 as cv
from cvzone.HandTrackingModule import HandDetector


class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, screen):
        cv.rectangle(screen, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                     (255, 235, 230), cv.FILLED)
        cv.rectangle(screen, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                     (255, 255, 255), 3)
        cv.putText(screen, self.value, (self.pos[0] + 26, self.pos[1] + 70),
                   cv.FONT_HERSHEY_COMPLEX, 2, (50, 50, 50), 2)

    def click(self, x1, y1):
        if self.pos[0] < x1 < self.pos[0] + self.width and \
                self.pos[1] < y1 < self.pos[1] + self.height:
            cv.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                         (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                         (255, 255, 255), cv.FILLED)
            cv.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv.FONT_HERSHEY_COMPLEX,
                       3, (225, 210, 86), 5)
            return True
        else:
            return False


cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)
buttonList = [["7", "8", "9", "C"],
              ["4", "5", "6", "-"],
              ["1", "2", "3", "+"],
              ["%", "0", "*", "="]]

bList = []
for x in range(4):
    for y in range(4):
        x_pos = x * 100 + 700
        y_pos = y * 100 + 150
        bList.append(Button((x_pos, y_pos), 100, 100, buttonList[y][x]))

myEq = ""
counter = 0

# buttonC = Button((1100, 150), 100, 100, "C")
while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    # cv.rectangle(img, (790, 120), (1210, 660), (50, 50, 50), cv.FILLED)

    cv.rectangle(img, (700, 30), (1100, 270), (180, 180, 180), cv.FILLED)
    cv.rectangle(img, (700, 30), (1100, 270), (255, 255, 255), 3)

    cv.putText(img, myEq, (702, 112), cv.FONT_HERSHEY_COMPLEX, 1.65, (50, 50, 50), 2)

    hands, img = detector.findHands(img, flipType=False)
    # buttonC.draw(img)
    for b in bList:
        b.draw(img)

    if hands:
        hand1 = hands[0]
        lmList = hand1['lmList']
        length, _, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
        x, y = lmList[8][0:2]

        if length < 60:
            for i, b in enumerate(bList):
                if b.click(x, y) and counter == 0:
                    val = buttonList[int(i % 4)][int(i / 4)]
                    if val == "=":
                        myEq = str(eval(myEq))
                    elif val == "C":
                        myEq = ""
                    else:
                        myEq += val
                    counter = 1

    if counter != 0:
        counter += 1
        if counter > 10:
            counter = 0

    cv.imshow("Cam", img)
    cv.waitKey(1)

#    elif val == "rt":
#      var = myEq == str(math.sqrt(float(myEq)))
# elif val == "sq":
#  var = myEq == math.pow(float(myEq), 2)
# ["C", "rt", "sq", "/"],
