#!/usr/bin/env python3
from eyetracker import EyeTracker
import imutils
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required=True, help="path to face casacade file")
ap.add_argument("-e", "--eye", required=True, help="path to eye cascade file")
ap.add_argument("-v", "--video", help="path to (optional) video file")
args = vars(ap.parse_args())

# Init the facetracker
et = EyeTracker(args["face"], args["eye"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
    
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    # if we are viewing a video and we did not grab a frame,
    # then we have readed the end of the video
    if args.get("video") and not grabbed:
        break
    # resize and convert to gray
    frame = imutils.resize(frame, width=600)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = et.track(gray)
    
    for r in rects:
        cv2.rectangle(frame, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), 2 )
    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()