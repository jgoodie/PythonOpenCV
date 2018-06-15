#!/usr/local/opt/python3/bin/python3
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required = True, help = "Path to cascade file")
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# load the cat detector Haar cascade, the detect cat faces
# in the input image
detector = cv2.CascadeClassifier(args["cascade"])
rects = detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(75,75))

print("I found {} cat(s)".format(len(rects)))
# print(rects)
# loop over the cat faces and draw a rectangle surrounding each
for (i, (x,y,w, h)) in enumerate(rects):
    cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
    cv2.putText(image, "Cat #{}".format(i+1), (x,y-10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,255), 2)
    
cv2.imshow("Cat Faces", image)
cv2.waitKey(0)

