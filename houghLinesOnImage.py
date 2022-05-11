import numpy as np
import argparse
import imutils
import glob
import cv2
import math

#filters and stuff
frame = cv2.imread("C:/Users/22ape/OneDrive - Marist College Ashgrove/digital/unit 3 robot/openCV test/renderedMazeWithH.jpg")
grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     #convert to gray scale
edgeFrame = cv2.Canny(grayFrame, 100, 250)      #this first number is sensitivity - the lower it is, the more sensitive it detects
blurred = cv2.GaussianBlur(grayFrame, (9, 9), 0)
lines = cv2.HoughLines(edgeFrame,1,np.pi/180,100) #change the 4th thing for sensitivity
#h template
template = cv2.imread("C:/Users/22ape/OneDrive - Marist College Ashgrove/digital/unit 3 robot/openCV test/h.jpg")
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]

found = None
angles = []

#calculate lines
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
        angleOfLine = round((np.pi/2 - theta)*57.3,3)
        angles.append(angleOfLine)
        angles = sorted(angles, key=abs)
        yint = rho/b
        #print(yint)
print(angles)

#find H
for scale in np.linspace(0.8, 2.0, 10)[::-1]:
		resized = imutils.resize(blurred, width = int(blurred.shape[1] * scale))
		r = blurred.shape[1] / float(resized.shape[1])
		if resized.shape[0] < tH or resized.shape[1] < tW:
			break
		edged = cv2.Canny(resized, 100, 150)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)        

		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
(_, maxLoc, r) = found
(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)

cv2.imshow('Input', frame)

c = cv2.waitKey(0)
