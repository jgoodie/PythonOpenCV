#!/usr/bin/env python3
import argparse
import imutils
import cv2

class CarDetect:
    def __init__(self, carCascadePath):
        self.carCascadePath = cv2.CascadeClassifier(carCascadePath)
    def detect(self, image, scaleFactor = 1.2, minNeighbors = 5, minSize = (30,30)):
        rects = self.carCascadePath.detectMultiScale(image, scaleFactor=scaleFactor,
                                                  minNeighbors=minNeighbors,
                                                  minSize=minSize,
                                                  flags = cv2.CASCADE_SCALE_IMAGE)
        return(rects)

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--car", required = True, help = "Path to car cascade file")
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = imutils.resize(image, width=800)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
cd = CarDetect(args["car"])
carRects = cd.detect(gray, scaleFactor=1.012, minNeighbors=4, minSize=(30,30))
print("I found {} cars".format(len(carRects)))

for (x, y, w, h) in carRects:
    cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
    
cv2.imshow("Cars", image)
cv2.waitKey(0)