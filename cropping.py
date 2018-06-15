#!/usr/local/opt/python3/bin/python3
from __future__ import print_function
import argparse
import cv2
import numpy as np
import imutilsJG

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original", image)
cv2.waitKey(0)
print(image.shape)

cropped = image[30:120, 240:335]
cv2.imshow("T-Rex Face", cropped)
cv2.waitKey()