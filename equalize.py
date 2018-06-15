#!/usr/local/opt/python3/bin/python3
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
eq = cv2.equalizeHist(image)
cv2.imshow("Histogram Equalization", np.hstack([image, eq]))
cv2.waitKey(0)