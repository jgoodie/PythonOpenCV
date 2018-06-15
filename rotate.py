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

(h,w) = image.shape[:2]
center = (w//2, h//2)

M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(image,M,(w,h))

cv2.imshow("Rotated by 45 Degrees", rotated)
cv2.waitKey(0)

M = cv2.getRotationMatrix2D(center, -90, 1.0)
rotated = cv2.warpAffine(image,M,(w,h))

cv2.imshow("Rotated by -90 Degrees", rotated)
cv2.waitKey(0)

rotated = imutilsJG.rotate(image, 180, None, 0.5)
cv2.imshow("Rotated by 180 Degrees and halved", rotated)
cv2.waitKey(0)