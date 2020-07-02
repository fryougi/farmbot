# -*- coding: utf-8 -*-
"""
Testing OCR (grab template locations/windows)

Needed: pip install pytesseract
Install tesseract.exe on Windows
Add C:\Programs\Tesseract-OCR to system path
"""

import cv2
import pytesseract
import time

# Load image
cvimage = cv2.imread('screencaps/frame0.png')
tmpl = cv2.imread('templates/blue/repeatquest.png')

# List of location windows
# (xtol, ytol)
# (xmin, ymin, xmax, ymax)

# Compute match
custom_config = r'--oem 3 --psm 6'
time_start = time.perf_counter()
print(pytesseract.image_to_string(tmpl, config=custom_config))
time_end = time.perf_counter()
seconds = time_end - time_start
print("{:f}".format(seconds))