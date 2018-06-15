#!/usr/local/opt/python3/bin/python3
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import argparse
import imutils
import cv2

class ColorLabeler:
    def __init__(self):
        # initialize the color dictionary, containing the color
        # name as the key and the RGB tuple as the value
        colors = OrderedDict({
            "red":(255,0,0),
            "green":(0,255,0),
            "blue":(0,0,255),
            "yellow":(255,255,0),
            "orange":(255,153,0)})
        # allocate memory for the L*a*b image, then initialize
        # the color names list
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames=[]
        # loop over the colors dictionary
        for (i, (name,rgb)) in enumerate(colors.items()):
            # update the L*a*b* array and the color names list
            self.lab[i] = rgb
            self.colorNames.append(name)
        # convert the L*a*b array from the RGB color space
        # to L*a*b
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)
    def label(self, image, c):
        # construct a mask for the contour, then compute the 
        # average L*a*b value for the masked reggion
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]
        # initialize the minimum distance found thus far
        minDist = (np.inf, None)
        # loop over the known L*a*b color values
        for (i, row) in enumerate(self.lab):
            # compute the distance between the current L*a*b
            # color value adn the mean of the image
            d = dist.euclidean(row[0], mean)
            # if the distance between the current L*a*b
            # color value and the mean of the image
            if d < minDist[0]:
                minDist = (d, i)
        # return the name of the color with the smallest distance
        return self.colorNames[minDist[1]]
    

class ShapeDetector:
    def __init__(self):
        pass
    def detect(self, c):
        # init the shape name and approximage the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04*peri, True)
        
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            print("[INFO] Triangle: {}".format(len(approx)))
            print("[INFO] CONTOUR AREA: {}".format(cv2.contourArea(c)))
            shape = "triangle"
        # if a shape has 4 vertices, it is either a square or rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use
            # bounding box to compute the aspect ratio
            (x,y,w,h) = cv2.boundingRect(approx)
            ar = w/float(h)
            # a square will have an spect ratio that is approximagely
            # equal to one, otherwise, the shape is a rectangle
            if ar >= 0.95 and ar <= 1.05:
                print("[INFO] Square: {}".format(len(approx)))
                print("[INFO] CONTOUR AREA: {}".format(cv2.contourArea(c)))
                shape = "square"
            else:
                print("[INFO] Rectangle: {}".format(len(approx)))
                print("[INFO] CONTOUR AREA: {}".format(cv2.contourArea(c)))
                shape = "rectangle"
        # if the shape is a pentagon,  it will have 5 vertices
        elif len(approx) == 5:
            print("[INFO] Pentagon: {}".format(len(approx)))
            print("[INFO] CONTOUR AREA: {}".format(cv2.contourArea(c)))
            shape = "pentagon"
#         elif len(approx) == 6:
#             print("[INFO] Hexagon: {}".format(len(approx)))
#             print("[INFO] CONTOUR AREA: {}".format(cv2.contourArea(c)))
#             shape = "hexagon"
#         elif len(approx) == 7:
#             print("[INFO] Septagon: {}".format(len(approx)))
#             print("[INFO] CONTOUR AREA: {}".format(cv2.contourArea(c)))
#             shape = "septagon"
#         elif len(approx) == 8:
#             print("[INFO] Octagon: {}".format(len(approx)))
#             print("[INFO] CONTOUR AREA: {}".format(cv2.contourArea(c)))
#             shape = "octagon"
        # otherwise, we assume the shape is a circle
        else:
            print("[INFO] Circle: {}".format(len(approx)))
            print("[INFO] CONTOUR AREA: {}".format(cv2.contourArea(c)))
            shape = "circle"
        return shape
    
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help = "Path to image file")
args = vars(ap.parse_args())   

# load the image and resize it to a smaller factor so that 
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
image = imutils.resize(image, width=800)
ratio = image.shape[0]/float(resized.shape[0])
print("[INFO] RATIO: {}".format(ratio))

# convert the resized image to grayscale, blur it slightly,
# and threshold it
blurred = cv2.GaussianBlur(resized, (5,5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
cv2.imshow("blurred", blurred)
cv2.imshow("thresh", thresh)

# find contours in the thresholded image and initialize the 
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = [0] if imutils.is_cv2() else cnts[1]
print("[INFO] SHAPES: {}".format(len(cnts)))

# Init the shape detector and color labeler
sd = ShapeDetector()
cl = ColorLabeler()

# loop over the contours
for c in cnts:
    # compute the center of the contour, then detect the name of the,
    # shape using only the contour
    M = cv2.moments(c)
    cX = int(M["m10"]/M["m00"] * ratio)
    cY = int(M["m01"]/M["m00"] * ratio)
    
    shape = sd.detect(c)
    color = cl.label(lab, c)
    
    # multiply the contour (x,y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape on the image
    c = c.astype("float")
    c = c * ratio
    #c *= ratio
    c = c.astype("int")
    text = "{} {}".format(color,shape)
    print("[INFO] COLOR: {}".format(color))
    cv2.drawContours(image, [c], -1, (0,255,0), 2)
    cv2.putText(image, shape, (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, (255,255,255), 1)
    
    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)


     
