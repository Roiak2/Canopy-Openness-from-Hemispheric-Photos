#!/usr/bin/env/python
"""
Class object ImageLoad() to process/load hemispheric photos 
provided by user as input.
"""

#Importing packages
import glob #helping identify files in pathfiles
import skimage #image manipulation
from skimage import io #loading and plotting image
from skimage.feature import canny #defining features within picture
from skimage.draw import circle_perimeter #circling function to create circle
from skimage.util import img_as_ubyte #image definitions
from skimage.filters import threshold_otsu #threshold otsu algorithm
from skimage.filters import threshold_isodata #threshold isodata algorithm
from skimage.color import rgb2gray # import rgb2gray
import pathlib #getting pathfiles
import pandas #dataframe manipulation and outputting
import numpy as np #statistical calculations
import os #finding pathfiles
import natsort #batch loading of files
import matplotlib.pyplot as plt #plots
from loguru import logger #logger 
    
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

# convert functions into one Class object to load and prepare images
class ImagePrep():
    """
    Class object to load image files and convert them to black and white to 
    differentiate sky from canopy objects
    """
    def __init__(self, filepath, filename,threshold=0,threshold_method="otsu"):
        """
        Initialize function by saving inputs and outputs in object
        """
        # store inputs and outputs in __init__
        # created empty strings for a number of self.___ definitions as a temporary placeholder
        # but would suggest finding a better/morespecific placeholder depending on data type of each object


        # inputs
        self.filepath = filepath
        self.filename = filename
        self.threshold = int(threshold) #manually set threshold, default is none
        self.threshold_method = threshold_method #threshold algorithm, defaults to otsu or can be isodata
        
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
        #Debugging logger message
        logger.debug(f"loaded image: {self.filename}")
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
        
        self.image = self.photo #setting image
        
        self.image[:,:,0] = 0 #changing channels
        self.image[:,:,1] = 0 
        #plot photo
        plt.imshow(self.image) 
        #debugging logger message
        logger.debug(f"converted image to blue...") 
        #return photo
        return self.image


    #function to turn blue image into thresholded black and white image
    def bwPic(self):
        """
        This function takes an image file as input, converts to greyscale, uses an algorithm (or manual input)
        to threshold, and then converts the photo into binary black and white based on that threshold.
        Outputs a new binary image and plots it
    
        PARAMETERS
        Inputted image file
        """
        #converting photo to grayscale
        self.gray_image = rgb2gray(self.image)
        #set threshold (if above threshold, array set to 1, otherwise 0 creating black-and-white),
        #   either manually with user input, or based on algorithms: otsu or isodata

        if self.threshold == 0 and self.threshold_method == "otsu": #if method is otsu, use that (default)
            self.threshold = threshold_otsu(self.gray_image)
        if self.threshold == 0 and self.threshold_method == "isodata": #if method is isodata, use that
            self.threshold = threshold_isodata(self.gray_image)
        else: #if manual threshold inserted, override algorithm and use manual threshold
            self.threshold = self.threshold
        
        #create new image 
        self.binary = self.gray_image > self.threshold
        #plots image
        plt.imshow(self.binary,cmap=plt.cm.gray)
        #debugging logger message
        logger.debug(f"converted image to BW ...threshold...")

        #print message to user displaying threshold and method used
        if self.threshold != 0:
            print("Threshold = ",round(self.threshold,2), "Method = User input")
        else:
            print("Threshold = ",round(self.threshold,2), "Method = ", self.threshold_method)
        
        #returns it
        return self.binary