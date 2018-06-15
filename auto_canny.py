#!/usr/local/opt/python3/bin/python3
import numpy as np
import argparse
import glob
import cv2


def auto_canny(image, sigma=0.33):
    # compute the media of the single channel pixel intensities
    v = np.median(image)
    
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0,(1.0-sigma)*v))
    upper = int(max(255,(1.0-sigma)*v))
    print("[INFO] v: {} | lower: {} | upper {}".format(v, lower, upper))
    edged = cv2.Canny(image, lower, upper)
    return(edged)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", help = "Path to image directory")
args = vars(ap.parse_args())

# loop over the images
for imagePath in glob.glob(args["images"] + "/*.jpg"):
    # load the image, convert it to grayscale and blur it slightly
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3,3), 0)
    
    # apply Canny edge detection using a wide threshold, tight
    # threshold, and automatically determined threshold
    wide = cv2.Canny(blurred, 10, 200)
    tight = cv2.Canny(blurred, 225, 250)
    auto = auto_canny(blurred)
    
    # show the images
    cv2.imshow("Original", image)
    cv2.imshow("Edges", np.hstack([wide, tight, auto]))
    cv2.waitKey(0)