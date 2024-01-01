import os
import time
from cvzone.HandTrackingModule import HandDetector
import cv2
from flask import Flask, render_template, Response, request

app = Flask(__name__)

cap = cv2.VideoCapture(0)
imgBackground = cv2.imread("static/Resources/Background.png")

# Importing all the mode images to a list
folderPathModes = "static/Resources/Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes = []
for imgModePath in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgModePath)))

# importing all the icons to a list
folderPathIcons = "static/Resources/Icons"
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = []
for imgIconsPath in sorted(listImgIconsPath)[:26]:  # Selecting first 26 icons
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIconsPath)))

# Define the menu prices
menuPrices = {
    1: [12, 17, 15, 10, 12, 10, 15, 15, 10, 15],
    2: [20, 15, 20, 10, 15, 15, 15, 10, 20, 15],
    3: [0, 0, 0],
    4: [0, 2, 4]
}

modeType = 0  # for changing selection mode
selection = -1
counter = 0
selectionSpeed = 20
detector = HandDetector(detectionCon=0.8, maxHands=2)
#modePositions = [(1205, 112), (882, 118), (1205, 226), (882, 232), (1205, 340), (882, 332), (1205, 464), (882, 432), (1205, 586), (882, 600)]
counterPause = 0
selectionList = [-1, -1, -1, -1]

checkoutMenu = []
modes4_completed = False
modes4_completed_time = 0

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    global imgBackground, cap, modeType, selection, counter, counterPause, selectionList, modes4_completed

    while True:
        success, img = cap.read()
        # Find the hand and its landmarks
        hands, img = detector.findHands(img)  # with draw
        # Overlay the webcam feed on the background image
        imgBackground[84:84 + 480, 50:50 + 640] = img
        imgBackground[0:720, 810:1280] = listImgModes[modeType]

        if hands and counterPause == 0 and modeType < 4:
            # Hand 1
            hand1 = hands[0]
            fingers1 = detector.fingersUp(hand1)
            print(fingers1)

            if fingers1 == [0, 1, 0, 0, 0]:
                if selection != 1:
                    counter = 1
                selection = 1
            elif fingers1 == [0, 1, 1, 0, 0]:
                if selection != 2:
                    counter = 1
                selection = 2
            elif fingers1 == [1, 1, 1, 0, 0]:
                if selection != 3:
                    counter = 1
                selection = 3
            elif fingers1 == [0, 1, 1, 1, 1]:
                if selection != 4:
                    counter = 1
                selection = 4
                if modeType == 2 or modeType == 3:
                    # Batasi pemilihan menu pada modes 3
                    selection = min(selection, 3)
            elif fingers1 == [1, 1, 1, 1, 1]:
                if selection != 5:
                    counter = 1
                selection = 5
                if modeType == 2 or modeType == 3:
                    # Batasi pemilihan menu pada modes 3
                    selection = min(selection, 3)
            elif fingers1 == [0, 1, 1, 1, 0]:
                if selection != 6:
                    counter = 1
                selection = 6
                if modeType == 2 or modeType == 3:
                    # Batasi pemilihan menu pada modes 3
                    selection = min(selection, 3)
            elif fingers1 == [0, 1, 1, 0, 1]:
                if selection != 7:
                    counter = 1
                selection = 7
                if modeType == 2 or modeType == 3:
                    # Batasi pemilihan menu pada modes 3
                    selection = min(selection, 3)
            elif fingers1 == [0, 1, 0, 1, 1]:
                if selection != 8:
                    counter = 1
                selection = 8
                if modeType == 2 or modeType == 3:
                    # Batasi pemilihan menu pada modes 3
                    selection = min(selection, 3)
            elif fingers1 == [0, 0, 1, 1, 1]:
                if selection != 9:
                    counter = 1
                selection = 9
                if modeType == 2 or modeType == 3:
                    # Batasi pemilihan menu pada modes 3
                    selection = min(selection, 3)
            elif fingers1 == [1, 0, 0, 0, 0]:
                if selection != 10:
                    counter = 1
                selection = 10
                if modeType == 2 or modeType == 3:
                    # Batasi pemilihan menu pada modes 3
                    selection = min(selection, 3)
            else:
                selection = -1
                counter = 0

            if counter > 0:
                counter += 1
                print(counter)

            #cv2.ellipse(imgBackground, modePositions[selection - 1], (53, 53), 0, 0,
                        #counter * selectionSpeed, (0, 255, 0), 10)

            if counter * selectionSpeed > 360:
                selectionList[modeType] = selection
                modeType += 1
                counter = 0
                selection = -1
                counterPause = 1

        # To pause after each selection is made
        if counterPause > 0:
            counterPause += 1
            if counterPause > 60:
                counterPause = 0

        # Modes 1
        if selectionList[0] != -1:
            imgBackground[611:611 + 65, 108:108 + 65] = listImgIcons[1 + selectionList[0] - 11]
        # Modes 2
        if selectionList[1] != -1:
            imgBackground[612:612 + 65, 263:263 + 65] = listImgIcons[1 + selectionList[1]]
        # Modes 3
        if selectionList[2] != -1:
            mode3Menu = min(selectionList[2], 3)  # Batasi pemilihan menu pada modes 3
            imgBackground[612:612 + 65, 415:415 + 65] = listImgIcons[13 + mode3Menu - 1]
        # Modes 4
        if selectionList[3] != -1:
            mode4Menu = min(selectionList[3], 3)  # Batasi pemilihan menu pada modes 4
            imgBackground[612:612 + 65, 566:566 + 65] = listImgIcons[16 + mode4Menu - 1]

        # Modes 5
        kosong = cv2.imread("static/Resources/Icons/kosong.png")
        if modeType == 4:
            if not modes4_completed:
                start_time = time.time()
                modes4_completed = True
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time <= 20:
                imgBackground[611:611 + 65, 108:108 + 65]
            else:
                modeType = 0
                selectionList = [-1, -1, -1, -1]
                imgBackground[612:612 + 65, 263:263 + 65] = kosong
                imgBackground[611:611 + 65, 108:108 + 65] = kosong
                imgBackground[612:612 + 65, 415:415 + 65] = kosong
                imgBackground[612:612 + 65, 566:566 + 65] = kosong

        if all(menu == -1 for menu in selectionList):
            checkoutMenu = []
        else:
            checkoutMenu = [menuPrices.get(modeType + 1, [])[menu - 1] for modeType, menu in enumerate(selectionList) if menu != -1]

        checkoutText = f"Total Pesanan: Rp{sum(checkoutMenu):.2f}"
        cv2.putText(imgBackground, checkoutText, (824, 690), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)

        # Displaying
        ret, buffer = cv2.imencode('.png', imgBackground)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)