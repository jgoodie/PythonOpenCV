#!/usr/local/opt/python3/bin/python3
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help = "Path to image file")
args = vars(ap.parse_args())

# load the image, convert it grayscale and blur it slightly
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred, 61, 255, cv2.THRESH_BINARY)[1]

# find the contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
print("I count {} shapes in this image".format(len(cnts)))

# loop over the contours
for c in cnts:
    # compute the center of the contour
    M = cv2.moments(c)
    cX = int(M["m10"]/M["m00"])
    cY = int(M["m01"]/M["m00"])
    
    # draw the contour and center of the shape on the image
    cv2.drawContours(image, [c], -1, (0,255,0),2)
    cv2.circle(image, (cX,cY), 7, (255,255,255), -1)
    cv2.putText(image, "center", (cX-20, cY-20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
    # show the image
    cv2.imshow("Image", image)
    cv2.waitKey(0)