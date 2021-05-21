#!/usr/bin/env/python
"""
Calculating fractions of sunlight (i.e. gap) in hemispheric photos and getting canopy openness metric for a photo
"""

#**What this module does**  
#  - 1) Takes black and white image segmented by ImageLoad.py with circle of fisheye calculated by FishEye.py
#  - 2) Segments each photo to 89 smaller circles
#  - 3) Calculates gap fraction or proportion of sky (i.e. 0 in numpy array value) within each circle and returns that list of 89 circles
#  - 4) Calculates proportion of entire fisheye photo that is sky (i.e. openness) based on those 89 gap fraction values
#  - 5) Returns the value of canopy openness for the hemispheric photo

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
class CanOpen():
    """
    Class object to get fractions of sunlight (i.e. gap) in hemispheric photos and getting canopy openness metric for a photo
    """
    #function to intialize the class object
    def __init__(self,fisheye,batch=False):
        """
        Initialize function by saving inputs and outputs in object
        """
        #input (image file from ImageLoad class object)
        self.fisheye = fisheye #image
        #self.shape = self.fisheye[0].shape #setting shape of image
        self.batch = batch #boolean, if true processing in batch so changes logger messages, defaults to false

        # get x,y and r of circle
        self.cx = self.fisheye[1]
        self.cy = self.fisheye[2]
        # #if the photo dimensions are small
        # if self.fisheye[0].shape[0] < 2000:
        #     #set tighter radius
        #     self.cr = int((self.cy/2)-350)
        # #if photo dimensions are normal
        # else:
        #     #set radius normally
        #     self.cr = self.fisheye[3]
        self.cr = self.fisheye[3]

        #variables for calculating gap fraction, area, and canopy openness
        self.gfp_radian = (np.pi / 180) * np.arange(360) #360 slices around 2*pi for gap fraction calculation
        self.open_radian = (np.pi / 180) * np.arange(89) #89 slices around 2*pi for openness calculation
        self.half_radian = (np.pi / 180) * 0.5 #half of a slice for calculating area of each of 89 circles and for entire hemispheric photo
        self.last_rad = self.open_radian[len(self.open_radian)-1] #getting last element in array for total fisheye area calculation
        self.first_rad = self.open_radian[1] #getting first element in array for total fisheye area calculation

        #outputs
        self.gap_fractions = np.zeros(89) #result of GapFraction function, initialized empty matrix of 89 to be filled
        self.canopy_openness = "" #empty integer to be filled with results

    #function to calculate gap fractions for 89 circles within hemispheric photo
    def calc_gap_fractions(self):
        """
        This function takes a black-and-white image array from FishEye.py with information on center circle and radius of hemispheric photo,
        then calculates the proportion of sky within 89 sub-circles within the fisheye.
        It does this by iterating over the 360 radian slices (gfp_radian), getting coordinates for sub-circle using trigonometry
            (x coordinate + cosine*radian slices for each circle by dividing the radius by 90)
            (y coordinate + sin*radian slices for each circle by dividing the radius by 90)

        Since the image array is divided into 0s (sky) and 1s (canopy), the code then goes through each sub-circle coordinates 
        and counts the amount of 1s there, returning an amount from 0-360 (i.e. for each degree in each sub-circle).
        Finally, that amount is divided by 360 for each sub-circle to normalize it and return a proportion  

        PARAMETERS
        self.fisheye = Black and white photo with information on fisheye circle coordinates and radius from FishEye.py
        self.cx = center x coordinates
        self.cy = center y coordinates
        self.cr = center radius
        self.gfp_radian = radian conversion for each degree in 360-degree circle

        OUTPUT
        self.gap_fractions = array of 89 sub-circle with value of proportion sky or gap in each sub-circle
        """

        # convert image array from boolean (False, True) to integer (0,1)
        self.fisheye[0] = self.fisheye[0].astype(int)

        # iterate over 89 sub circles within fisheye
        for step in range(89):
            x = self.cx + np.round(np.cos(self.gfp_radian) * step * self.cr / 90, 0) #calculate x coordinates of each sub circle
            y = self.cy + np.round(np.sin(self.gfp_radian) * step * self.cr / 90, 0) #calculate y coordinates of each sub circle
            #iterate over 360 degree slices 
            for degree in range(360):
                ydeg = y[degree] #get iteration of y array
                xdeg = x[degree] #get iteration of x array
                self.gap_fractions[step] +=  self.fisheye[0][int(np.round(ydeg,3)), int(np.round(xdeg,3))] #calculate proportion sky from image array and insert into gap fraction empty matrix

        #if only processing single image
        if self.batch == False:
            # logger debugging statement
            logger.debug(f"Calculating gap fraction profile for sub-circles")
        
        # return gap fraction normalized by 360 degrees
        self.gap_fractions = self.gap_fractions / 360

        return self.gap_fractions
    
    #function to calculate gap fractions for 89 circles within hemispheric photo
    def openness(self):
        """
        This function takes the self.gap_fractions array of proportion sky for 89 sub-circles in a fisheye photo,
        and then multiplies that by the area of each sub circle and divides by the total area of the fisheye photo.
        This yields a single value of the proportion sky (i.e. canopy openness) in a single photo

        PARAMETERS
        self.last_rad = the radian from the 89th sub-circle
        self.first_rad = the radian from the 1st sub-circle
        self.open_radian = the radians for all the sub-circles 
        self.gap_fractions = the array of proportion sky for each of the 89 sub-circles

        OUTPUT
        self.openness = proportion (from 0 to 1) of sky in hemispheric photo, 0 being completely closed and 1 being completely open
        """

        #Total area of fisheye circle
        Atot = np.sin(self.last_rad + self.half_radian) - np.sin(self.first_rad - self.half_radian) #sin of last sub=circle + half radian minus first sub-circle

        #Area of all the sub-circles (returns array)
        Aa = np.sin(self.open_radian + self.half_radian) - np.sin(self.open_radian - self.half_radian) #same calculation but for each sub-circle

        #Calculating canopy openness from gap fraction array
        self.canopy_openness = np.sum(self.gap_fractions * Aa / Atot) #sum gap fraction array times each sub-circle area normalized by total area of photo
        
        #if only processing single image
        if self.batch == False:
            # logger debugging statement
            logger.debug(f"Calculating openness for single hemispheric photo")
            print('Canopy Openness = ', self.canopy_openness)

        # return canopy openness
        return self.canopy_openness
