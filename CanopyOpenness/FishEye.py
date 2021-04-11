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
from skimage.draw import line, set_color #setting colors
import matplotlib.cbook #getting matplot lib cookbook
import warnings #warnings package
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation) #suppress specific annoying warning
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

#class object to get the boundaries of the fisheye lens for openness calculations
class FishEye():
    """
    Class object to get center coordinates, radius of fisheye lens and output new image array with that information
    """
    #function to intialize the class object
    def __init__(self,fisheye,cx=0,cy=0,cr=0,plot=False,batch=False):
        """
        Initialize function by saving inputs and outputs in object
        """
        #input (image file from ImageLoad class object)
        self.fisheye = fisheye #image
        self.shape = self.fisheye.shape #setting shape of image

        #center coordinates of the fisheye lens to exclude border
        self.cx = cx #center x
        self.cy = cy #center y
        self.cr = cr #center radius
        self.rr = "" #radius for circle_perimeter function in skimage
        self.cc = "" #center coordinates for circle_perimeter function in skimage
        self.plot = plot #boolean, if true plots images, otherwise won't, defaults to False
        self.batch = batch #boolean, if true means we're batch processing so different print messages, defaults to False
        
        #output of new image with center coordinates added
        self.ImageCircle = "" #correct image
        self.ImageCircle2 = "" #numpy array assigned with circle_perimeter (not sure this workd)
        self.circleImage = "" #output of manually set center coordinates and radius in SetCircle function
        self.circleImage2 = "" #same as circleImage but different format

    #function for adding center coordinates of image and radius of center
    def CircleCoords(self):
        """
        Function that takes an image as input and returns image file with circle of fisheye lens as boundary
        Based on calculating of center coordinates given the shape of the numpy array (file format of image)
        
        PARAMETERS
        self.fisheye = input loaded image
        self.shape = shape of input image
        self.cx = center x coordinate
        self.cy = center y coordinate
        self.cr = radius of center circle of fisheye lens
        self.rr and self.cc = inputs for circle_perimeter function in skimage
        
        OUTPUT
        self.ImageCircle = image array with coordinates for center circle of fisheye photo
        plots image with circle drawn in red
        self.ImageCircle2 = how circle_perimeter function says to index into numpy array (not sure it works though)
        """
        #SET COORDINATES AND RADIUS
        #x coordinate of center
        self.cx = int(self.shape[1]/2)
        #y coordinate of center
        self.cy = int(self.shape[0]/2)
        #radius of the hemispheric photo center
        self.cr = int((self.shape[0]/2)-150)

        #if only processing single image
        if self.batch == False:
            #Print message displaying coordinates and radius to user
            print('center circle coordinates = (',self.cx,',',self.cy,')', 'radius = ',self.cr) 

        #ADD TO NUMPY ARRAY
        #draw circle perimeter based on above coordinates and radius
        self.rr, self.cc = circle_perimeter(self.cy,self.cx, radius=self.cr, shape=self.shape) 
        #put all those in a list with new coordinates
        self.ImageCircle = [self.fisheye,self.cx,self.cy,self.cr]
        #Assigning to numpy array another way for plotting
        self.ImageCircle2 = self.fisheye[self.rr,self.cc] = 1 

        #if only processing single image
        if self.batch == False:
            #logger debugging statement
            logger.debug(f"Set center circle...fisheye...coordinates")
        
        #plotting for user to see the circle around the fisheye if plot is true
        if self.plot == True:
            #Create circle for plotting based on coordinates, color red
            circle = plt.Circle((self.cx, self.cy), self.cr, color=(1, 0, 0),fill=False)
            #create subplots
            fig, ax = plt.subplots()
            #In figure, Image as background
            plt.imshow(self.ImageCircle[0], cmap=plt.cm.gray)
            # Add the circles to figure as subplots
            ax.add_patch(circle)
  
        #return new format of image
        return self.ImageCircle#, self.ImageCircle2

    #function for setting circle manually, otherwise leaving as is
    def SetCircle(self,cx=0,cy=0,cr=0):
        """
        Function that manually sets image coordinates based on previous calculations of center circle of hemispheric image
        
        PARAMETERS
        self.circleImage = image after it's gone through CircleCoords function (self.ImageCircle)
        self.cx = center x coordinate
        self.cy = center y coordinate
        self.cr = radius of center circle of fisheye lens

        OUTPUT
        self.circleImage, image with center coordinates and radius, also plots to show user
        """
        #intializing photo
        self.circleImage = self.fisheye
        
        #center coordinates of the fisheye lens to exclude border
        self.cx = cx #center x
        self.cy = cy #center y
        self.cr = cr #center radius

        #if coordinates are not set manually, set them from CircleCoords function
        if(self.cx==0):
            self.cx = self.ImageCircle[1]
        if(self.cy==0):
            self.cy = self.ImageCircle[2]
        if(self.cr==0):
            self.cr = self.ImageCircle[3]

        #ADD TO NUMPY ARRAY
        #draw circle perimeter based on above coordinates and radius
        self.rr, self.cc = circle_perimeter(self.cy,self.cx, radius=self.cr, shape=self.shape) 
        #put all those in a list with new coordinates
        self.circleImage = [self.fisheye,self.cx,self.cy,self.cr]
        #Assigning to numpy array another way for plotting
        self.circleImage2 = self.fisheye[self.rr,self.cc] = 1 
        
        #if only processing single image
        if self.batch == False:
            #logger debugging statement
            logger.debug(f"Manually setting fisheye coordinates",self.cx)
            #Print message displaying coordinates and radius to user
            print('center circle coordinates = (',self.cx,',',self.cy,')', 'radius = ',self.cr) 
        
        #plotting for user to see the circle around the fisheye if plot is true
        if self.plot == True:
            #Create circle for plotting based on coordinates, color red
            circle = plt.Circle((self.cx, self.cy), self.cr, color=(1, 0, 0),fill=False)
            #create subplots
            fig, ax = plt.subplots()
            #In figure, Image as background
            plt.imshow(self.circleImage[0], cmap=plt.cm.gray)
            # Add the circles to figure as subplots
            ax.add_patch(circle)

        #return new format of image
        return self.circleImage #, self.circleImage2