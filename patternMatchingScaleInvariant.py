import numpy as np
import argparse
import imutils
import glob
import cv2

xVals = []
cumX = 0


cap = cv2.VideoCapture(0)

template = cv2.imread("C:/Users/22ape/OneDrive - Marist College Ashgrove/digital/unit 3 robot/openCV test/h.jpg")
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
cv2.imshow("Template", template)


while True:
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	found = None

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

	# draw a bounding box around the detected result and display the image
	cv2.rectangle(blurred, (startX, startY), (endX, endY), (0, 0, 255), 2)
	cv2.imshow("Image", blurred)
	#cv2.imshow("Image", edged)
	key = cv2.waitKey(1)
	if key == ord('q'):
		break
	#print((endX-startX)/2 + startX)
	#print((endY-startY)/2 + startY)

	newX=(endX-startX)/2 + startX
	xVals.append(newX)
	if len(xVals) >= 30:
		xVals.pop(0)
	for i in range(len(xVals)):
		cumX += xVals[i]
	averageX = cumX/30
	cumX = 0
	print(averageX)
