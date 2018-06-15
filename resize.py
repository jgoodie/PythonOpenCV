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

# We want to resize the image width to 150 
# We also need to set a ratio to maintain the aspect ratio
# r = ratio 
# Multiply width ratio times height to maintain aspect ratio
# r = 150.0/image.shape[1]
# dim = (150, int(image.shape[0]*r))
# 
# resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
# cv2.imshow("Resized-Width", resized)
# cv2.waitKey()
# 
# # Resize by height and set the height ratio
# r = 50.0/image.shape[0]
# dim = (int(image.shape[1]*r), 50)
# 
# resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
# cv2.imshow("Resized-Height", resized)
# cv2.waitKey()
# 
# resized = imutilsJG.resize(image, width=100)
# cv2.imshow("Resized-Width-Func", resized)
# cv2.waitKey()
# 
# resized = imutilsJG.resize(image, height=50)
# cv2.imshow("Resized-Height-Func", resized)
# cv2.waitKey()


# r = 66/image.shape[1]
# dim = (66, int(image.shape[0]*r))
# print(int(image.shape[0]*r))
# resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
# cv2.imshow("Resized-Width", resized)
# cv2.waitKey()

# Resize by height and set the height ratio
r = 110/image.shape[0]
dim = (int(image.shape[1]*r), 110)
print(dim)
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("Resized-Height", resized)
cv2.waitKey()