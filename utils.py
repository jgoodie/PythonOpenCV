#!/usr/local/opt/python3/bin/python3
import numpy as np
import cv2

def centroid_histogram(clt):
    # grad the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0,len(np.unique(clt.labels_))+1)
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)
    # Normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum() # hist = hist/hist.sum()
    return(hist)

def plot_colors(hist, centroids):
    # init the bar chart representing the relative freq
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype = "uint8" )
    startX = 0
    
    # loop over the precentage of each cluster and the color 
    # of each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX),0), (int(endX),50),color.astype("uint8").tolist(), -1)
        startX = endX
    return(bar)
