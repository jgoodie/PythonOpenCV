#!/usr/bin/env python3
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


ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required = True, help = "Path to face cascade file")
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
#image = cv2.imread("http://192.168.255.26/camera/oneshotimage")
image = imutils.resize(image, width=800)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

fd = FaceDetector(args["face"])
faceRects = fd.detect(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (30,30))

print("I found {} face".format(len(faceRects)))

for (x, y, w, h) in faceRects:
    cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
    
cv2.imshow("Faces", image)
cv2.waitKey(0)
