import cv2 as cv
import cv2.aruco as aruco

cap = cv.VideoCapture(0)
font = cv.FONT_HERSHEY_SIMPLEX

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

# how many pixels the center of the tag needs to be from the center of the frame before the robot starts turning
turnThresh = 50

# the size of the tag in px^2 at which point the robot goes backwards
maxAcceptableArea = 30000
# the size of the tag in px^2 at which point the robot goes forwards
minAcceptableArea = 15000

while True:
    ok, frame = cap.read()

    # get frame dimensions
    height, width, channels = frame.shape

    # get center of width of frame
    centerW = int(width / 2)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # check if there are any markers in frame
    if ids is None:
        # if not, give an error message
        cv.putText(frame, "Looking for marker with ID 0", (0, 20), font, 1, (0, 0, 255), 2, 1)
        cv.putText(frame, "Stopping...", (0, 40), font, 1, (0, 0, 255), 2, 1)
    else:
        count = 0
        # if so, check the values of all the ids
        for currentId in ids:
            # check if the current id has a value of 0
            if int(currentId) != 0:
                # if not, give an error message
                cv.putText(frame, "Looking for marker with ID 0", (0, 20), font, 1, (0, 0, 255), 2, 1)
                cv.putText(frame, "Stopping...", (0, 40), font, 1, (0, 0, 255), 2, 1)
            else:
                # if so, calculate center position
                # get the bounding box of the marker
                currentBbox = corners[count][0]

                # get the corner points
                p1 = tuple(currentBbox[0])  # top left
                p2 = tuple(currentBbox[1])  # top right
                p3 = tuple(currentBbox[2])  # bottom right
                p4 = tuple(currentBbox[3])  # bottom left

                # draw the bounding box
                cv.line(frame, p1, p2, (0, 255, 0), 2, 1)
                cv.line(frame, p2, p3, (0, 255, 0), 2, 1)
                cv.line(frame, p3, p4, (0, 255, 0), 2, 1)
                cv.line(frame, p4, p1, (0, 255, 0), 2, 1)

                # draw the tag data
                cv.putText(frame, "ID: " + str(currentId), p1, font, 0.5, (255, 0, 0), 2, 1, )

                # find the midpoint
                mid = (int((p3[0] + p1[0]) / 2), int((p3[1] + p1[1]) / 2))

                # draw the midpoint
                cv.line(frame, mid, mid, (0, 0, 255), 8, 1)

                # find the area
                w = p2[0] - p1[0]
                h = p3[1] - p2[1]
                area = w * h

                # determine if the tag is off center and if so how much to turn by
                # TODO: add implementation for motor control
                # if the center of the tag is to the right of the center of the screen, turn right
                if mid[0] > centerW + turnThresh:
                    cv.putText(frame, "turn right", (0, 20), font, 1, (0, 0, 255), 2)
                elif mid[0] < centerW - turnThresh:
                    cv.putText(frame, "turn left", (0, 20), font, 1, (0, 0, 255), 2)
                else:
                    cv.putText(frame, "centered", (0, 20), font, 1, (0, 0, 255), 2)

                # TODO: add implementation for motor control
                # use the area of the tag to figure out whether to go forward or backward
                if area > maxAcceptableArea:
                    cv.putText(frame, "go backward", (0, 40), font, 1, (0, 0, 255), 2)
                elif area < minAcceptableArea:
                    cv.putText(frame, "go forward", (0, 40), font, 1, (0, 0, 255), 2)
                else:
                    cv.putText(frame, "stay put", (0, 40), font, 1, (0, 0, 255), 2)

                # increment counter by 4
                count += 4

    cv.imshow("Snack Cart Auton", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
