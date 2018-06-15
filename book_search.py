#!/usr/bin/env python3
from coverdescriptor import CoverDescriptor
from covermatcher import CoverMatcher
import argparse
import glob
import csv 
import cv2

ap =argparse.ArgumentParser()
ap.add_argument("-d", "--db", required = True, help = "path to the book db")
ap.add_argument("-c", "--covers", required = True, help = "dir path to book covers")
ap.add_argument("-q", "--query", required = True, help = "path to query book covers")
ap.add_argument("-s", "--sift", type = int, default = 0, help = "use SIFT?" )
args = vars(ap.parse_args())

db = {}

for l in csv.reader(open(args["db"])):
    db[l[0]] = l[1:]
    
useSIFT = args["sift"] > 0
useHamming = args["sift"] == 0
ratio = 0.7
minMatches = 40

if useSIFT:
    minMatches = 50

cd = CoverDescriptor(useSIFT=useSIFT)
cv = CoverMatcher(cd, glob.glob(args["covers"]+"/*.png"),
        ratio = ratio, minMatches = minMatches, useHamming = useHamming)
queryImage = cv2.imread(args["query"])
gray = cv2.cvtColor(queryImage, cv2.COLOR_BGR2GRAY)
(queryKps, queryDescs) = cd.describe(gray)
results = cv.search(queryKps, queryDescs)
cv2.imshow("Query", queryImage)

if len(results) == 0:
    print("I couldn't find a match for that cover.")
    cv2.waitKey(0)
else:
    for (i, (score, coverPath)) in enumerate(results):
        (author, title) = db[coverPath[coverPath.rfind("/") + 1:]]
        print("{}. {:.2f}% : {} - {}".format(i +1, score*100, author, title))
        result = cv2.imread(coverPath)
        cv2.imshow("Result", result)
        cv2.waitKey(0)

