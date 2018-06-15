#!/usr/local/opt/python3/bin/python3
import argparse
import imutils
import cv2

class FaceDetector:
    def __init__(self, faceCascadePath):
        self.faceCascade = cv2.CascadeClassifier(faceCascadePath)
    
    def detect(self, image, scaleFactor = 1.2, minNeighbors = 5, minSize = (30,30)):
        rects = self.faceCascade.detectMultiScale(image, scaleFactor=scaleFactor,
                                                  minNeighbors=minNeighbors,
                                                  minSize=minSize,
                                                  flags = cv2.CASCADE_SCALE_IMAGE)
        return(rects)

# construct the arguement parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "Path to (optional) video file")
ap.add_argument("-f", "--face", required = True, help = "Path to face cascade file")
args = vars(ap.parse_args())

# Init the face detector
fd = FaceDetector(args["face"])


# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
    #camera = cv2.VideoCapture("http://192.168.2.101/camera/image")

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
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceRects = fd.detect(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (30,30))
    frameClone = frame.copy() 
    for (x, y, w, h) in faceRects:
        cv2.rectangle(frameClone, (x,y), (x+w, y+h), (0,255,0), 2)
    
    # show the frame to our screen
    cv2.imshow("Face", frameClone)
    key = cv2.waitKey(1) & 0xFF
    
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
    
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows() 
