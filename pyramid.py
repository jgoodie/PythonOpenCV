#!/usr/local/opt/python3/bin/python3
from helpers import pyramid
from skimage.transform import pyramid_gaussian
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to image")
ap.add_argument("-s", "--scale", type=float, default=1.5, help="scale factor size")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

# METHOD #1: No smooth, just scaling
# Loop over the image pyramid
for (i, resized) in enumerate(pyramid(image, scale=args["scale"])):
    # show the resized image
    cv2.imshow("Layer {}".format(i+1), resized)
    cv2.waitKey(0)
    
    
# close all the windows
cv2.destroyAllWindows()

# METHOD 2: Resizing + Gaussian smoothing
for (i, resized) in enumerate(pyramid_gaussian(image,downscale=2)):
    # if the image is too small, break from the loop
    if resized.shape[0] < 30 or resized.shape[1] < 30:
        break
    # show the resized image
    cv2.imshow("Layer {}".format(i+1), resized)
    cv2.waitKey(0)

# close all the windows
cv2.destroyAllWindows()