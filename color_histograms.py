#!/usr/local/opt/python3/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original", image)

# split out the channels
chans = cv2.split(image)
colors = ("b", "g", "r")
# print(len(chans[0]))
# print(len(chans[1]))
# print(len(chans[2]))

plt.figure()
plt.title("'Flattend' Color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")

# chans is a list of 3 lists -> B,G,R
# colors is just the tuple of b, g and r
# zip creates a 3 tuples combined with colors and chans 
# [(b,chans[0]),(g,chans[1]),(r,chans[2])]
for (chan, color) in zip(chans, colors):
    hist = cv2.calcHist([chan], [0], None, [256], [0,256])
    plt.plot(hist, color = color)
    plt.xlim([0,256])

# fig = plt.figure()
# ax = fig.add_subplot(131)
# hist = cv2.calcHist([chans[1], chans[0]], [0,1], None, [32,32], [0,256,0,256])
# p = ax.imshow(hist, interpolation = "nearest")
# ax.set_title("2D Color Histogram for G and B")
# plt.colorbar(p)

# fig = plt.figure()
# ax = fig.add_subplot(132)
# hist = cv2.calcHist([chans[1], chans[2]], [0,1], None, [32,32], [0,256,0,256])
# p = ax.imshow(hist, interpolation = "nearest")
# ax.set_title("2D Hist for G & R")
# plt.colorbar(p)

fig = plt.figure()
ax = fig.add_subplot(132)
hist = cv2.calcHist([chans[1], chans[2]], [0,1], None, [8,8], [0,256,0,256])
p = ax.imshow(hist, interpolation = "nearest")
ax.set_title("2D Hist for G & R")
plt.colorbar(p)


# fig = plt.figure()
# ax = fig.add_subplot(133)
# hist = cv2.calcHist([chans[0], chans[2]], [0,1], None, [32,32], [0,256,0,256])
# p = ax.imshow(hist, interpolation = "nearest")
# ax.set_title("2D Color Histogram for B and R")
# plt.colorbar(p)

print("2D Histogram shape: {}, with {} values".format(hist.shape, hist.flatten().shape[0]))

hist = cv2.calcHist([image],[0,1,2], None, [8,8,8], [0,256,0,256,0,256])
print("3D histogram shape: {}, with {} values".format(hist.shape, hist.flatten().shape[0]))

plt.show()    
cv2.waitKey(0)    
