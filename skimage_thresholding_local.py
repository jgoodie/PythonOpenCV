#!/usr/local/opt/python3/bin/python3
from skimage.filters import threshold_otsu, threshold_local
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
ratio = image.shape[0]/500
orig = image.copy()
image = imutils.resize(image, height=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

global_thresh = threshold_otsu(gray)
binary_global = (gray > global_thresh).astype("uint8")*255

block_size = 35
adaptive_thresh = threshold_local(gray, block_size, offset=10)
binary_adaptive = (gray > adaptive_thresh).astype("uint8")*255

cv2.imshow("Original", image)
cv2.imshow("Global Thresholding", binary_global)
cv2.imshow("Adaptive Thresholding", binary_adaptive)
cv2.waitKey(0)