#!/usr/bin/env/python
"""
Defining fisheye center circle coordinates for future gap fraction calculation
"""

#**What this module does**  
#  - 1) Takes black and white image segmented by ImageLoad.py  
#  - 2) Calculates circle of fisheye lens from center coordinates and radius
#  - 3) Outputs image array with coordinates 

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#Importing packages
import glob #helping identify files in pathfiles
import os #finding pathfiles
from loguru import logger #Logger for debugging messages
import pathlib #getting pathfiles
import pandas #dataframe manipulation and outputting
import numpy as np #statistical calculations
import natsort #batch loading of files
import matplotlib.pyplot as plt #plots

import skimage #image manipulation
from skimage import io #filepaths in skimage
from skimage.feature import canny #making shapes in images
from skimage.draw import circle_perimeter #drawing circles
from skimage.util import img_as_ubyte #saving images
from skimage.filters import threshold_otsu #threshold algorithm
from skimage.color import rgb2gray #grayscale

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

#adding class object to get the boundaries of the fisheye lens for openness calculations
class FishEye():
    """
    Class object to get center coordinates, radius of fisheye lens and output new image array with that information
    """
    #function to intialize the class object
    def __init__(self,fisheye):
        """
        Initialize function by saving inputs and outputs in object
        """
        #store inputs and outputs in __init__

        #input (image file from ImageLoad class object)
        self.fisheye = fisheye
        
        #center coordinates of the fisheye lens to exclude border
        self.cx = "" 
        self.cy = ""
        self.cr = ""
        
        #output of new image with center coordinates added
        self.ImageCircle = ""
        self.circleImage = ""

    #function for adding center coordinates of image and radius of center
    def CircleCoords(self):
        """
        Function that takes an image as input and returns image file with circle of fisheye lens as boundary
        Based on calculating of center coordinates given the shape of the numpy array (file format of image)
        
        PARAMETERS
        image = input loaded image
        
        OUTPUT
        returns image array with coordinates for center circle of fisheye photo
        """
        #x coordinate of center
        self.cx = self.fisheye.shape[1]/2
        #y coordinate of center
        self.cy = self.fisheye.shape[0]/2
        #radius of the hemispheric photo center
        self.cr = (self.fisheye.shape[0]/2)-2
        #put all those in a list with new coordinates
        self.ImageCircle = [self.fisheye,self.cx,self.cy,self.cr]

        #logger debugging statement
        logger.debug(f"Set center circle...fisheye...coordinates")
        #plotting to check
        plt.imshow(self.ImageCircle[0],cmap=plt.cm.gray)
        #return new format of image
        #return self.ImageCircle

    #function for setting circle based on the calculated center circle radius
    def SetCircle(self):
        """
        Function that sets image coordinates based on previous calculations of center circle of hemispheric image
        
        PARAMETERS
        self.image = image after it's gone through CircleCoords function
        self.cx = center x coordinate
        self.cy = center y coordinate
        self.cr = radius of center circle of fisheye lens
        """
        #intializing photo from ImageCircle
        self.circleImage = self.ImageCircle

        #if coordinates greater than 0, set them as center circle coordinates for image file
        if(self.cx>0):
            self.circleImage[1] = self.cx
        if(self.cy>0):
            self.circleImage[2] = self.cy
        if(self.cr>0):
            self.circleImage[3] = self.cr
        
        #logger debugging statement
        logger.debug(f"Assuring center fisheye coordinates are above 0")
        #plotting to check
        plt.imshow(self.circleImage[0],cmap=plt.cm.gray)
        #return new format of image
        return self.circleImage