#!/usr/bin/env python3
import imutils
import cv2

camera = cv2.VideoCapture("rtsp://192.168.1.9:8554/unicast")

while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    
    # resize the frame
    #frame = imutils.resize(frame, width=600)
    
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()