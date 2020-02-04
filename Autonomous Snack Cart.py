import cv2 as cv
import pyzbar.pyzbar as zbar

# get the video capture
vid = cv.VideoCapture(0)

# get the font
font = cv.FONT_HERSHEY_SIMPLEX

# this is the pixel threshold that is used to determine when to adjust course by turning
turnThresh = 50

maxAcceptableTagSize = 30000
minAcceptableTagSize = 15000

while True:
    # get a frame
    ret, frame = vid.read()

    # get frame dimensions
    height, width, channels = frame.shape

    # convert that frame to gray to make qr processing easier
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # get a list of qr codes in the grayscale image, looking only for qr codes
    detectedQr = zbar.decode(gray, symbols=[zbar.ZBarSymbol.QRCODE])

    for qr in detectedQr:
        # get the tag data
        data = str(qr.data)

        # check that the tag is in fact the follow tag
        if data == "b'follow me'":
            # get the bounding box
            (x, y, w, h) = qr.rect

            # get the horizontal center of the qr code
            centerX = (x + (x + w)) / 2

            # get the horizontal center of the frame
            centerFrame = width / 2

            # get the are of the tag
            area = w * h

            # draw the bounding box in red with a width of 1
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            # also draw text near the bounding box with the code's data on it
            cv.putText(frame, data + str(area), (x, y), font, 1, (0, 0, 255), 2)

            # determine if the tag is off center and if so how much to turn by
            # TODO: add implementation for motor control
            # if the center of the tag is to the right of the center of the screen, turn right
            if centerX > centerFrame + turnThresh:
                cv.putText(frame, "turn right", (0, 20), font, 1, (0, 0, 255), 2)
            # if the center of the tag is to the left of the center of the screen, turn left
            elif centerX < centerFrame - turnThresh:
                cv.putText(frame, "turn left", (0, 20), font, 1, (0, 0, 255), 2)
            else:
                cv.putText(frame, "centered", (0, 20), font, 1, (0, 0, 255), 2)

            # TODO: add implementation for motor control
            # use the area of the tag to figure out whether to go forward or backward
            if area > maxAcceptableTagSize:
                cv.putText(frame, "go backward", (0, 40), font, 1, (0, 0, 255), 2)
            elif area < minAcceptableTagSize:
                cv.putText(frame, "go forward", (0, 40), font, 1, (0, 0, 255), 2)
            else:
                cv.putText(frame, "stay put", (0, 40), font, 1, (0, 0, 255), 2)

    cv.imshow("Autonomous snack cart", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()
