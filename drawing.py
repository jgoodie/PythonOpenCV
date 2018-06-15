#!/usr/local/opt/python3/bin/python3
from __future__ import print_function
import cv2
import numpy as np

# INIT THE CANVAS
# we are representing our image as an RGB image with pixels
# in the range [0, 255], it’s important that we use an 8-bit unsigned
# integer, or uint8.
canvas = np.zeros((300,300,3), dtype = 'uint8')
print(canvas.shape)

green = (0,255,0)
cv2.line(canvas, (0,0), (300,300), green)
cv2.imshow("canvas", canvas)
cv2.waitKey(0)

red = (0,0,255)
cv2.line(canvas, (300,0), (0,300), red)
cv2.imshow("canvas", canvas)
cv2.waitKey(0)

blue = (255,0,0)
cv2.rectangle(canvas, (10,10), (60,60), blue)
cv2.imshow("canvas", canvas)
cv2.waitKey(0)

purple = (255,0,255)
cv2.rectangle(canvas, (50,200), (200,225), purple, 5)
cv2.imshow("canvas", canvas)
cv2.waitKey(0)

pleep = (200, 42, 100)
cv2.rectangle(canvas, (200,50), (225,125), pleep, -1)
cv2.imshow("canvas", canvas)
cv2.waitKey(0)


# Re-INIT the Canvas
canvas = np.zeros((300,300,3), dtype = 'uint8')
(centerX, centerY) = (canvas.shape[1]//2, canvas.shape[0]//2)
white = (255,255,255)

for r in range(0,175,25):
    cv2.circle(canvas, (centerX, centerY), r, white)

cv2.imshow("canvas", canvas)
cv2.waitKey(0)

for i in range(0,50):
    radius = np.random.randint(5, high=20)
    color = np.random.randint(0, high=256, size=(3,)).tolist()
    pt = np.random.randint(0, high=300, size=(2,))
    cv2.circle(canvas, tuple(pt), radius, color, -1)
cv2.imshow("canvas", canvas)
cv2.waitKey(0)

