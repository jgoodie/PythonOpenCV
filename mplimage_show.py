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
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#image = mpimg.imread("foo.jpg")
#print(image.shape)

image = cv2.imread("cat.jpg")

plt.axis("off")
#plt.imshow(image)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()