#!/usr/bin/env python3
import numpy as np
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())

blueLower = np.array([100,67,0], dtype="uint8")
blueUpper = np.array([255,128,50], dtype="uint8")

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

while True:
    (grabbed, frame) = camera.read()
    
    if not grabbed:
        break
    # resize the video
    frame = imutils.resize(frame, width=600)
    # Create a black and white Threshold based on the blue boundaries
    blue = cv2.inRange(frame, blueLower, blueUpper)
    # blur it to make finding contours more accurate
    blue = cv2.GaussianBlur(blue, (3,3), 0)
    # find the contours
    (_, cnts, _) = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL, 
                                    cv2.CHAIN_APPROX_SIMPLE)
    # sort the contours, grab the largest bounding rects and draw them
    if(len(cnts)>0):
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        rect = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))
        cv2.drawContours(frame, [rect], -1, (0,255,0),2)
    cv2.imshow("Tracking", frame)
    cv2.imshow("Binary",blue)
    # time.sleep(0.025)
    if(cv2.waitKey(1) & 0xFF == ord("q")):
        break

camera.release()
cv2.destroyAllWindows()
    

