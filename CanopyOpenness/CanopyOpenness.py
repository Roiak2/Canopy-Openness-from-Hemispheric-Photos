#!/usr/bin/env/python
"""
Calculating fractions of sunlight (i.e. gap) in hemispheric photos and getting canopy openness metric for a photo
"""

#**What this module does**  
#  - 1) Takes black and white image segmented by ImageLoad.py with circle of fisheye calculated by FishEye.py
#  - 2) Segments each photo to 89 smaller circles
#  - 3) Calculates gap fraction or proportion of sky (i.e. 0 in numpy array value) within each circle and returns that list of 89 circles
#  - 4) Calculates proportion of entire fisheye photo that is sky (i.e. openness) based on those 89 gap fraction values
#  - 5) Returns the value of canopy openness (will eventually be stored with photo name and info in a csv)

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#Importing packages
import glob #helping identify files in pathfiles
import os #finding pathfiles
import pathlib #getting pathfiles
import pandas #dataframe manipulation and outputting
import numpy as np #statistical calculations
import natsort #batch loading of files
import skimage #image manipulation
from skimage import io #filepaths in skimage
import warnings #warnings package
from loguru import logger #Logger for debugging messages
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

#class object to calculate gap fractions in image and compute proportion openness
class CanopyOpenness():
    """
    Class object to get fractions of sunlight (i.e. gap) in hemispheric photos and getting canopy openness metric for a photo
    """
    #function to intialize the class object
    def __init__(self,fisheye,cx=0,cy=0,cr=0):
        """
        Initialize function by saving inputs and outputs in object
        """
        #input (image file from ImageLoad class object)
        self.fisheye = fisheye #image
        self.shape = self.fisheye.shape #setting shape of image

        #center coordinates of the fisheye lens to exclude border (default to 0 but can be manually adjusted)
        self.cx = cx #center x
        self.cy = cy #center y
        self.cr = cr #center radius

        #variables for calculating gap fraction, area, and canopy openness
        self.gfp_radian = np.pi / 180 * np.arange(360) #360 slices around 2*pi for gap fraction calculation
        self.open_radian = np.pi / 180 * np.arange(89) #89 slices around 2*pi for openness calculation
        self.half_radian= np.pi / 180 * 0.5 #half of a slice for calculating area of each of 89 circles and for entire hemispheric photo

        #outputs
        self.gap_fractions = np.zeros(89) #result of GapFraction function, initialized empty matrix of 89 to be filled
        self.openness = int() #empty integer to be filled with results

    #function to calculate gap fractions for 89 circles within hemispheric photo
    def calc_gap_fractions(self):
        """
        This function takes a black-and-white image array from FishEye.py with information on center circle and radius of hemispheric photo,
        then calculates the proportion of sky within 89 sub-circles within the fisheye 

        PARAMETERS
        self.fisheye = Black and white photo with information on fisheye circle coordinates and radius from FishEye.py

        """
        # convert image array from boolean (False, True) to integer (0,1)
        self.fisheye[0] = self.fisheye[0].astype(int)

        # get x,y and r of circle
        self.cx = self.fisheye[1]
        self.cy = self.fisheye[2]
        self.cr = self.fisheye[3]

        # iterate over 89 sub circles within fisheye
        for step in range(89):
            x = self.cx + np.round(np.cos(self.gfp_radian) * step * self.cr / 90, 0) #calculate x coordinates of each sub circle
            y = self.cy + np.round(np.sin(self.gfp_radian) * step * self.cr / 90, 0) #calculate y coordinates of each sub circle
            #iterate over 360 degree slices 
            for degree in range(360):
                ydeg = y[degree] #get iteration of y array
                xdeg = x[degree] #get iteration of x array
                self.gap_fractions[step] +=  self.fisheye[0][int(np.round(ydeg,3)), int(np.round(xdeg,3))] #calculate proportion sky from image array and insert into gap fraction empty matrix

        #logger debugging statement
        logger.debug(f"Calculating gap fraction profile for sub-circles")

        #return gap fraction normalized by 360 degrees
        return self.gap_fractions / 360