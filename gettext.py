# -*- coding: utf-8 -*-
"""
Testing OCR (grab template locations/windows)

Install pytesseract for python:
  pip install pytesseract
Install tesseract.exe on Windows
  (https://tesseract-ocr.github.io/tessdoc/Home.html)
  (https://github.com/tesseract-ocr/tesseract)
Add C:\Programs\Tesseract-OCR to system path
  My Computer -> System -> Advanced Settings -> Environment Variables
"""

import cv2
import pytesseract
import time

# Load image
cvimage = cv2.imread('screencaps/battle.png')
cvframe = cvimage[8:40,854:924]

# List of location windows
# (xtol, ytol)
# (xmin, ymin, xmax, ymax)
cvframe = cv2.cvtColor(cvframe, cv2.COLOR_BGR2GRAY)
cvframe = cv2.threshold(255-cvframe, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#cv2.imshow('cvimage', cvframe)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Compute match
time_start = time.perf_counter()
wave = pytesseract.image_to_string(cvframe, config=r'-l eng --oem 3 --psm 7')
time_end = time.perf_counter()
seconds = time_end - time_start
print("{} {:f}".format(wave, seconds))