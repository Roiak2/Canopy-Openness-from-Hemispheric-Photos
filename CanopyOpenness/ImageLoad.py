#!/usr/bin/env/python
"""
Class object ImageLoad() to process/load hemispheric photos 
provided by user as input.
"""

#Importing packages
import skimage #image manipulation
from skimage import io
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
from skimage.filters import threshold_otsu #threshold algorithm
import pathlib #getting pathfiles
import pandas #dataframe manipulation and outputting
import numpy as np #statistical calculations
import glob #helping identify files in pathfiles
import os #finding pathfiles
import natsort #batch loading of files
import matplotlib.pyplot as plt #plots

# add rgb2gray 
from skimage.color import rgb2gray # import rgb2gray

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

# convert functions into one Class object to load and prepare images
class ImagePrep():
    """
    Class object to load image files and convert them to black and white to 
    differentiate sky from canopy objects
    """
    def __init__(self, filepath, filename):
        """
        Initialize function by saving inputs and outputs in object
        """
        # store inputs and outputs in __init__
        # created empty strings for a number of self.___ definitions as a temporary placeholder
        # but would suggest finding a better/morespecific placeholder depending on data type of each object


        # inputs
        self.filepath = filepath
        self.filename = filename
        
        # store outputs from imageLoad
        self.photo_location = ""
        self.photo = ""   
        
        # input for BluePic (uses self.photo from imageLoad)
        # output for BluePic
        self.image = ""
        
        # input for bwPic (uses self.image from BluePic)
        # output for bwPic
        self.gray_image = ""
        self.th = ""
        self.binary = ""
        
    
    #function to load image and plot it    
    def imageLoad(self):
        """
        This function takes a filepath and filename of an image and loads 
        that image and returns it and plots it
        PARAMETERS
        filepath - where image is stored (a directory)
        filename - name of image (with jpg, png ending)
        """
        #uploading photo based on given path and image name
        self.photo_location = os.path.join(self.filepath, self.filename) 
        #reading image file using io.imread from skimage
        self.photo = io.imread(self.photo_location) 
        #plot photo
        plt.imshow(self.photo)
        #return photo
        return self.photo

    #function to convert image to blue channel
    def BluePic(self):
        """
        This function converts a loaded image into just the blue from RGB channel.
        Outputs image file with just blue channel and plots it
    
        PARAMETERS
        input - image file
        """
        #setting only blue channel by setting R and G (0 and 1 indexed in numpy array of image file) to 0 
        
        self.image = self.photo
        
        self.image[:,:,0] = 0
        self.image[:,:,1] = 0
        #plot photo
        plt.imshow(self.image)  
        #return photo
        return self.image


    #function to turn blue image into thresholded black and white image
    def bwPic(self):
        """
        This function takes an image file as input, converts to greyscale, uses an algorithm 
        to threshold, and then converts the photo into binary black and white based on that threshold.
        Outputs a new binary image and plots it
    
        PARAMETERS
        Inputted image file
        """
        #converting photo to grayscale
        self.gray_image = rgb2gray(self.image)
        #set threshold based on otsu algorithm (if above threshold, array set to 1, otherwise 0 creating black-and-white)
        self.th = threshold_otsu(self.gray_image)
        #Create new image 
        self.binary = self.gray_image > self.th
        #plots image
        plt.imshow(self.binary,cmap=plt.cm.gray)
        #returns it
        return self.binary