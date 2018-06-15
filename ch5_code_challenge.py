#!/usr/local/opt/python3/bin/python3
import cv2
import numpy as np
canvas = np.zeros((300,300,3), dtype = 'uint8')
red = (0,0,255)
green = (0,255,0)
for row in range(0,300,20):
    for col in range(10,300,20):
        cv2.rectangle(canvas, (col,row), (col+10,row+10), red, -1)
for row in range(10,300,20):
    for col in range(0,300,20):
        cv2.rectangle(canvas, (col,row), (col+10,row+10), red, -1)
cv2.circle(canvas, (canvas.shape[1]//2, canvas.shape[0]//2), canvas.shape[1]//5, green,-1)
cv2.imshow("canvas", canvas)
cv2.waitKey(0)