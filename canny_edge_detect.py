#!/usr/local/opt/python3/bin/python3
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "Path to image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image, (5,5), 0)
cv2.imshow("Blurred", image)

#canny = cv2.Canny(image, 30, 150)
canny = cv2.Canny(image, 10, 200)
cv2.imshow("Canny", canny)
cv2.waitKey(0)