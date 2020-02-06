import cv2 as cv
import cv2.aruco as aruco
import numpy as np
import sys

cap = cv.VideoCapture(0)
font = cv.FONT_HERSHEY_SIMPLEX

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

while True:
    ok, frame = cap.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # check if there are any markers in frame
    if ids is None:
        # if not, give an error message
        cv.putText(frame, "Can't find marker...", (0, 20), font, 1, (0, 0, 255), 2, 1)
    else:
        count = 0
        # if so, check the values of all the ids
        for currentId in ids:
            # check if the current id has a value of 0
            if int(currentId) != 0:
                # if not, give an error message
                cv.putText(frame, "Can't find marker...", (0, 20), font, 1, (0, 0, 255), 2, 1)
            else:
                # if so, calculate center position
                # get the bounding box of the marker
                currentBbox = corners[count][0]

                # get the corner points
                p1 = tuple(currentBbox[0])  # p1 will always be the top left of the marker
                p2 = tuple(currentBbox[1])
                p3 = tuple(currentBbox[2])
                p4 = tuple(currentBbox[3])

                # draw the bounding box
                cv.line(frame, p1, p2, (0, 255, 0), 2, 1)  # top left
                cv.line(frame, p2, p3, (0, 255, 0), 2, 1)
                cv.line(frame, p3, p4, (0, 255, 0), 2, 1)
                cv.line(frame, p4, p1, (0, 255, 0), 2, 1)

                # draw the tag data
                cv.putText(frame, "ID: " + str(currentId), p1, font, 0.5, (255, 0, 0), 2, 1, )

                # draw the top left point
                cv.line(frame, p1, p1, (0, 0, 255), 4, 1)

                # increment counter by 4
                count += 4

    cv.imshow("Snack Cart Auton", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
