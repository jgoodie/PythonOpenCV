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

# 1,0 == pixels x (left/right), 0,1 == pixels y (up,down)
M = np.float32([[1,0,25],[0,1,50]])
shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
cv2.imshow("Shifted Down and Right", shifted)
cv2.waitKey(0)

# Shifted left and up
M = np.float32([[1,0,-50],[0,1,-90]])
shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
cv2.imshow("Shifted Up and Left", shifted)
cv2.waitKey(0)

shifted = imutilsJG.translate(image, 0, 100)
cv2.imshow("Shifted Down", shifted)
cv2.waitKey(0)