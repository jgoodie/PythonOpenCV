#!/usr/bin/env python3
import numpy as np
import argparse
import imutils
import cv2

# construct the arguement parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "Path to (optional) video file")
ap.add_argument("-f", "--face", required = True, help = "Path to face cascade file")
args = vars(ap.parse_args())

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
    
# initialize a rectangular and square structuring kernel
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13,5))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21,21))

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
    # Init the face cascade and get the face rectangles
    faceCascade = cv2.CascadeClassifier(args["face"])
    faceRects = faceCascade.detectMultiScale(gray, scaleFactor=1.2,
        minNeighbors=5, minSize=(30,30),
        flags = cv2.CASCADE_SCALE_IMAGE)
    # smooth the image using a 3x3 Gaussian, then apply the blackhat
    # morphological operator to find dark region on a light background
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
    
    # compute the Scharr gradient of the blackhat image and scale the
    # result into the range [0,255]
    gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX-minVal)/(maxVal-minVal))).astype("uint8")
    
    # apply a closing operation using the rectangular kernel to close
    # gaps in between letters -- then apply Otsu's thresholding method
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # perform another closing operation, this time using the square
    # kernel to close the gaps between lines of the MRZ, then perform a
    # series of erosions to break apart connected components
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
    thresh = cv2.erode(thresh, None, iterations=4)
    
    # during thresholding, it's possible that border pixels were
    # included in the thresholding, so let's set 5% of the left and 
    # right borders to zero
    p = int(frame.shape[1] * 0.05)
    thresh[:, 0:p]=0
    thresh[:, frame.shape[1]-p:]=0
    
    # find contours in the thresholded image and sort them by their
    # size
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    # print("[INFO] number of contours is: {}".format(len(cnts))) 
    for c in cnts:
        # compute the bounding box of the contour and use the contour to 
        # compute the aspect ratio and coverage ratio of the bounding box
        # width to the width of the image
        (x,y,w,h) = cv2.boundingRect(c)
        ar = w/float(h)
        crWidth = w/float(gray.shape[1])
        print("[INFO] coverage ratio is: {}".format(crWidth))
        # check to see if the aspect ratio and coverage width are within
        # acceptable criteria
        # if ar > 5 and crWidth > 0.75:
        if ar > 2 and crWidth > 0.005:
            # pad the bounding box since we applied erosions and now need
            # to regrow it
            pX = int((x+w)*0.03)
            pY = int((y+h)*0.03)
            (x,y) = (x-pX, y-pY)
            (w,h) = (w+(pX*2), h+(pY*2))
            
            # extract the ROI from the image and draw a bounding box
            # surrounding the MRZ
            roi = frame[y:y+h, x:x+w].copy()
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)
            
    # Draw the face rectangle
    for (x, y, w, h) in faceRects:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
    
    
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows() 