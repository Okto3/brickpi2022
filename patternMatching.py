import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv.imread('C:/Users/22ape/OneDrive - Marist College Ashgrove/digital/unit 3 robot/openCV test/veryEasyH.jpg')

img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('C:/Users/22ape/OneDrive - Marist College Ashgrove/digital/unit 3 robot/openCV test/h.jpg',0)
w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv.imwrite('res.png',img_rgb)

cv.waitKey(0) 

cv.destroyAllWindows()
