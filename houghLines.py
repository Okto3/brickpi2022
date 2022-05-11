import numpy as np
import argparse
import imutils
import glob
import cv2
import math

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     #convert to gray scale

    edgeFrame = cv2.Canny(grayFrame, 200, 250)      #this first number is sensitivity - the lower it is, the more sensitive it detects
    lines = cv2.HoughLines(edgeFrame,1,np.pi/180,100) #change the 4th thing for sensitivity

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(frame, pt1, pt2, (255,255,255), 3, cv2.LINE_AA)

    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:     #press escape to exit
        break

cap.release()
cv2.destroyAllWindows()
