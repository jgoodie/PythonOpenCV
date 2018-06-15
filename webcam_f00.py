#!/usr/local/opt/python3/bin/python3
import numpy as np
import argparse
import imutils
import cv2

# construct the arguement parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "Path to (optional) video file")
args = vars(ap.parse_args())

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
    #camera = cv2.VideoCapture("http://192.168.255.26/camera/image")

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
    

# keep looping
while True:
    # grab the current fram
    (grabbed, frame) = camera.read()
    
    # if we are viewing a video and we did not grab a frame,
    # then we have readed the end of the video
    if args.get("video") and not grabbed:
        break
    
    # resize the frame
    frame = imutils.resize(frame, width=600)
    
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows() 
