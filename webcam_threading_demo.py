#!/usr/local/opt/python3/bin/python3

#Special note for OSX users: I’ve run into a limitation in opencv on OSX, 
# the command cv2VideoCapture(0) can only be issued in the main threadSpecial 
# note for OSX users: I’ve run into a limitation in opencv on OSX, the command 
# cv2VideoCapture(0) can only be issued in the main thread
# See here for official code sample:
# https://github.com/opencv/opencv/blob/master/samples/python/video_threaded.py

from WebcamVideoStream import WebcamVideoStream
from FPS import FPS
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
    help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
    help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

# grab a pointer to the video stream
print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(0)
fps = FPS().start()

# loop over the specified number of frames
while fps._numFrames < args["num_frames"]:
    # grab the frame from the stream and resize it to have a maximum
    # width of 400 pixels
    (grabbed, frame) = stream.read()
    frame = imutils.resize(frame, width=400)
    
    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        
    # update the FPS counter
    fps.update()

# top the timer and display the FPS info
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# clean up
stream.release()
cv2.destroyAllWindows()

# create a *threaded video stream, allow the camera sensor to warmup, 
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

# loop over the specified number of frames
while fps._numFrames < args["num_frames"]:
    # grab the frame from the stream and resize it to have a maximum
    # width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    
    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    
    # update the FPS counter
    fps.update()
    
# top the timer and display the FPS info
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# clean up
vs.stop()
cv2.destroyAllWindows()





