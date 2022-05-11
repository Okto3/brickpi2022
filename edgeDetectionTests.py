import numpy as np
import argparse
import imutils
import glob
import cv2

cap = cv2.VideoCapture(0)

template = cv2.imread("C:/Users/22ape/OneDrive - Marist College Ashgrove/digital/unit 3 robot/openCV test/h.jpg")
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")


def findH(grayFrame):
    (tH, tW) = template.shape[:2]
    for scale in np.linspace(0.1, 2.0, 20)[::-1]:
        resizedImage = imutils.resize(grayFrame, width = int(grayFrame.shape[1] * scale))
        r = grayFrame.shape[1] / float(resizedImage.shape[1])

        if resizedImage.shape[0] < tH or resizedImage.shape[1] < tW:
            break

        edged = cv2.Canny(resizedImage, 50, 200)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result) 

        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.imshow("Image", frame)
    cv2.waitKey(1)
    print((endX-startX)/2 + startX)
    print((endY-startY)/2 + startY)
	
    

while True:
    ret, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     #convert to gray scale
    blurred = cv2.GaussianBlur(grayFrame, (9, 9), 0)
    edgeFrame = cv2.Canny(blurred, 20, 200)      #this first number is sensitivity - the lower it is, the more sensitive it detects

    cv2.imshow('Input', edgeFrame)

    #findH(grayFrame)

    c = cv2.waitKey(1)
    if c == 27:     #press escape to exit
        break

cap.release()
cv2.destroyAllWindows()