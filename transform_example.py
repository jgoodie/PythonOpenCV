#!/usr/local/opt/python3/bin/python3
from transform import four_point_transform
import numpy as np
import argparse
import cv2

# construct the command line args and parse the args
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the image")
ap.add_argument("-c", "--coords", help = "comma seperated list of source points")
args = vars(ap.parse_args())

# load the image and grab the source coordinates (i.e the list of
# (x, y) points
# NOTE: using the eval function is bad form, but for this example
# let's roll with it
image = cv2.imread(args["image"])
pts = np.array(eval(args["coords"]), dtype="float32")

# apply the four point transform to obtain a "birds eye view" of the image
warped = four_point_transform(image, pts)

# show the original  and warped images
cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)

