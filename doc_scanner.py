#!/usr/local/opt/python3/bin/python3
from transform import four_point_transform
import imutils
from skimage.filters import threshold_local # threshhold_adaptive has been depricated
import numpy as np # this was unused
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height 
# to the new height, clone it and resize it
image = cv2.imread(args["image"])
ratio = image.shape[0]/500
orig = image.copy()
image = imutils.resize(image, height=500)

# convert the image to greyscale, blur it, and find the edges in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)
edged = cv2.Canny(gray, 75, 200)

# show the original and the edge detected image
print("STEP 1: Edge detection")
cv2.imshow("Original", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

# find the contours in the edged image, keeping only the 
# largest ones, and initialize the screen contour
(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

# loop over the contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02*peri, True)
    
    # if our approximaged contour has four points, then we
    # can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break

# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
cv2.drawContours(image, [screenCnt], -1, (0,255,0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# apply the four point transform to obtain a top-down
# view of the original
warped = four_point_transform(orig, screenCnt.reshape(4,2)*ratio)

# convert the warped image to grayscale, then threshold it
# to give it that "black and white" paper effect
warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
# warped = threshold_adaptive(warped, 251, offset=10)
# warped = warped.astype("uint8")*255
block_size = 35
warped = threshold_local(warped_gray, block_size, offset=10)
warped_adaptive = (warped_gray > warped).astype("uint8")*255
# warped = cv2.adaptiveThreshold(warped, 251, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)
# warped = warped.astype("uint8")


# show the original as scanned images
print("STEP 3: Apply perspective transform")
cv2.imshow("Original", imutils.resize(orig, height=650))
cv2.imshow("Scanned", imutils.resize(warped_adaptive, height=650))
cv2.waitKey(0)



