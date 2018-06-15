#!/usr/local/opt/python3/bin/python3
import numpy as np
import argparse
import cv2

# construct the command line args and parse the args
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the image")
args = vars(ap.parse_args())

# load the image and convert it to greyscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# compute the Scharr gradient magnitude representation of the images
# in both the x and y direction
gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx=0, dy=1, ksize=-1)

# subtract the y-gradient from the x-gradient
gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

# blur and threshold the image
blured = cv2.blur(gradient, (9,9))
(_, thresh) = cv2.threshold(blured, 225, 255, cv2.THRESH_BINARY)

# construct a closing kernel and apply it to the thresholded image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21,7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# try to close the blobs by performing a series of erosions and dilations
closed = cv2.erode(closed, None, iterations=4)
closed = cv2.dilate(closed, None, iterations=4)

# find the contours of the barcoded region of the image
# find the contours in the thresholded image, then sort the contours
# by their area, keeping only the largest one
# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
#                        cv2.CHAIN_APPROX_SIMPLE)[-2]
(_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
box = np.int0(cv2.boxPoints(rect))

# draw a bounding box around the detected barcode and display the image
cv2.drawContours(image, [box], -1, (0,255,0), 3)

# cv2.imshow("gradX", gradX)
# cv2.imshow("gradY",gradY)
# cv2.imshow("gray", gray)
# cv2.imshow("gradient", gradient)
# cv2.imshow("blur and thresh", thresh)
# cv2.imshow("close", closed)
cv2.imshow("Image", image)
cv2.waitKey(0)