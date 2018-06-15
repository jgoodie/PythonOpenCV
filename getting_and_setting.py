#!/usr/local/opt/python3/bin/python3
from __future__ import print_function
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
# ap.add_argument("-s", "--save", required = True, help = "Path/Name of new image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original", image)
cv2.waitKey(0)

# Get the pixel [row, col]; image[Y,X]
# NOTE: BLUE, GREEN, RED
(b,g,r) = image[0,0]
print("Pixel at (0,0) - Red: {}, Green: {}, Blue: {}".format(r,g,b))

# Set the pixel
# NOTE: image[Y,X]
image[0,0] = (0,0,255)

(b,g,r) = image[0,0]
print("Pixel at (0,0) - Red: {}, Green: {}, Blue: {}".format(r,g,b))

# Get a section of the image
corner = image[0:100, 0:100]
cv2.imshow("Corner", corner)
cv2.waitKey(0)

# Set the section of the image
image[0:100, 0:100] = (0,255,0)
cv2.imshow("Updated", image)
cv2.waitKey(0)

image[0,0] = (0,0,255)

(b,g,r) = image[219,90]
print("Pixel at (219,90) - Red: {}, Green: {}, Blue: {}".format(r,g,b))
