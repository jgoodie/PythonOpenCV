#!/usr/local/opt/python3/bin/python3
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2

# construct the arguement parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "Path to (optional) video file")
ap.add_argument("-p", "--shape-predictor", required=True, 
                help="path to facial landmark predictor")
args = vars(ap.parse_args())

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
    
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

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
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        (x, y, w, h) = face_utils.rect_to_bb(rect)
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255, 0), 2)
    
        #cv2.putText(frame, "Face #{}".format(i+1), (x-10, y-10), 
        #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        for (x, y) in shape:
            cv2.circle(frame, (x,y), 1, (0,0,255), -1)
    
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows() 