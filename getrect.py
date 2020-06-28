# -*- coding: utf-8 -*-
"""
Testing OpenCV (grab template locations/windows)
"""

import numpy
import cv2

# Load image
cvimage = cv2.imread('screencaps/frame20.png')
tmpl = cv2.imread('templates/blue/repeatquest.png')
#mask = cv2.imread('templates/blue/mcskillmask.png')

# for nox
#cvframe = cvimage[33:33+720,1:1281] # full
#cvframe = cvimage[482:482+405,2:722] # vert
#cvframe = cvimage[42:42+720,2:1282] # blue
cvframe = cvimage # screencap

# List of location windows
# (xtol, ytol)
# (xmin, ymin, xmax, ymax)

# Compute match
h,w,_ = tmpl.shape
data = numpy.zeros((h,w,3),dtype=numpy.uint8)
#res = cv2.matchTemplate(cvframe, tmpl, cv2.TM_CCORR_NORMED, data, mask)
res = cv2.matchTemplate(cvframe, tmpl, cv2.TM_CCORR_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
# Get box
top_left = max_loc
bottom_right = (top_left[0]+w, top_left[1]+h)
cv2.rectangle(cvframe, top_left, bottom_right, 255, 2)
rect = (top_left[0],top_left[1],bottom_right[0],bottom_right[1])
print(rect)
print(max_val)
# Display
cv2.imshow('cvimage', cvframe)
cv2.waitKey(0)
cv2.destroyAllWindows()