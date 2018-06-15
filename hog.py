#!/usr/bin/env python3
from skimage import feature

# orientations defines how many gradient orientations will be in each historgram (bins)
# pixelsPerCell defines the number of pixels that will fall into each cell
# the image will be partitioned into multiple cells, each of pixelsPerCellxpixelsPerCell
# A histogram of gradient magnitudes will then be computed for each cell
# HOG will then normalize each of the histograms according to the number of cells that
# fall into each block using the cellsPerBlcok argument.

class HOG:
    def __init__(self, orientations = 9, pixelsPerCell = (8,8),
                 cellsPerBlock = (3,3), transform = False):
        self.orientations = orientations
        self.pixelsPerCell = pixelsPerCell
        self.cellsPerBlock = cellsPerBlock
        self.transform = transform
        
    def describe(self, image):
        hist = feature.hog(image, orientations=self.orientations,
                           pixels_per_cell=self.pixelsPerCell,
                           cells_per_block=self.cellsPerBlock,
                           transform_sqrt=self.transform)
        return(hist)
    

