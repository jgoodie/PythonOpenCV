#!/usr/local/opt/python3/bin/python3
from __future__ import print_function
import argparse
import cv2
# import mahotas
# import sklearn as skl
# import skimage as ski
# import numpy as np
# import pandas as pd
# import scipy as sp
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
ap.add_argument("-s", "--save", required = True, help = "Path/Name of new image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

print("width: {} pixels".format(image.shape[1]))
print("height: {} pixels".format(image.shape[0]))
print("channels: {} pixels".format(image.shape[2]))

cv2.imshow("Image", image)
cv2.waitKey(0)

cv2.imwrite(args["save"], image)