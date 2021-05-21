#!/usr/bin/env/python
"""
Module to run ImagePrep, FishEye, and CanopyOpenness on all images in a directory, i.e. "batch mode"
"""

#**What this module does**  
#  - 1) Takes a directory of images as input (filepath)
#  - 2) Iterates through each image in the directory and runs: 
#       - ImagePrep (loads, thresholds, bw conversion)
#       - FishEye (outline circle of fisheye lens to get coordinates)
#       - CanopyOpenness (calculate fraction sky of image)
#  - 3) Saves the value of canopy openness as well as image information in a csv file and returns to user as output

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#Importing packages
import CanopyOpenness #our package
from CanopyOpenness import ImageLoad #image load
from CanopyOpenness import FishEye #fisheye calculation
from CanopyOpenness import CanOpen #canopy openness calculation
import glob #helping identify files in pathfiles
import os #finding pathfiles
import pathlib #getting pathfiles
import pandas as pd #dataframe manipulation and outputting
import numpy as np #statistical calculations
import natsort #batch loading of files
import skimage #image manipulation
from skimage import io #filepaths in skimage
import warnings #warnings package
from loguru import logger #Logger for debugging messages
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

# A Class object to run ImageLoad, FishEye, and CanOpen on every image in a given directory and output dataframe csv
class BatchRun():
    """
    Class object to run ImageLoad, FishEye, and CanOpen on an entire directory of image files
    """
    # Function to initialize class object
    def __init__(self, dirpath, filepath, filename, save=False):
        """
        Initialize function by saving inputs and outputs in object
        """
        # store inputs and outputs in __init__

        # inputs
        self.dirpath = dirpath #where directory of images is 
        self.filepath = filepath #directory where user wants to save dataframe
        self.filename = filename #if user saves dataframe, name of that dataframe (has to end in '.csv')
        self.save = save #boolean, if True, will save resultant dataframe, if False no, defaults to False

        # outputs
        self.savepath = os.path.join(self.filepath, self.filename) # where user wants to save
        self.images = [f for f in os.listdir(dirpath) if f.endswith('JPG')] #list all jpeg files in a directory
        self.images.sort() #sort them
        self.results = [] #initialize empty list to store results
        self.df = pd.DataFrame(columns=['Plot','Subplot','Date','Exposure','Focus','Openness']) #initializing empty dataframe

        # dataframe output (iterate through images)
        for image in self.images:
            #if camera focus information is available
            if image.count('.')==5:
                #include all 5 columns in dataframe
                self.df['Plot'] = [i.split('.')[0] for i in self.images]  # get first item in list of images
                self.df['Subplot'] = [i.split('.')[1] for i in self.images]  # get subplot information (second item)
                self.df['Date'] = [i.split('.')[2] for i in self.images]  # get date information (third item)
                self.df['Exposure'] = [i.split('.')[3] for i in self.images]  # get exposure information (fourth item)
                self.df['Focus'] = [i.split('.')[4] for i in self.images] # get focus (manual or auto) information (fifth item)
            #if camera focus information is not available
            else:
                #don't split string on focus since it doesn't exist
                self.df['Plot'] = [i.split('.')[0] for i in self.images]  # get first item in list of images
                self.df['Subplot'] = [i.split('.')[1] for i in self.images]  # get subplot information (second item)
                self.df['Date'] = [i.split('.')[2] for i in self.images]  # get date information (third item)
                self.df['Exposure'] = [i.split('.')[3] for i in self.images]  # get exposure information (fourth item

    # Function to iterate through directory and get dataframe of openness values for each image in directory 
    def Batch(self):
        """
        This function iterates over all the image files and running ImagePrep, FishEye, and CanOpen modules 
        to calculate openness for each image.
        Then storing those values in the empty column in the dataframe containing the image metadata.
        Finally storing the resultant dataframe as a csv for the user
        """
        # for loop iterating through each image in directory
        for image in self.images:
            #load image and threshold using isodata algorithm, don't plot, set to batch
            img = ImageLoad.ImagePrep(self.dirpath,image,threshold_method="isodata",plot=False,batch=True)
            #load image
            og = img.imageLoad()
            #turn blue 
            blue = img.BluePic()
            #threshold algorithm and turn to black and white
            bw = img.bwPic()
                
            #set fisheye coordinates for center lens, don't plot, set to batch
            fish = FishEye.FishEye(bw,plot=False,batch=True)
            #save image array with coordinates
            fishy = fish.CircleCoords()
                
            #run canopy openness module, set to batch
            gfp = CanOpen.CanOpen(fishy,batch=True) #running module
            gaps = gfp.calc_gap_fractions() #calculating array of proportion sky for 89 sub-circles within fisheye lens
            openness = gfp.openness() #openness calculation
                
            #print message to user
            #print("Image",image, "processed")
            # logger debugging statement
            logger.debug(f"Image {image} Processed")

            #appending to result list
            self.results.append(openness)

        # append values from result to the dataframe with metadata of images
        self.df['Openness'] = self.results
        # logger debugging statement
        logger.debug(f"Dataframe successfully created")

        # return the resultant dataframe to the user
        return self.df
    
    # Function to save dataframe to file
    def SaveDF(self):
        """
        This function takes the resultant dataframe made above and saves to file with user input
        """

        # if user doesn't want to save
        if self.save == False:
            # return dataframe and do nothing
            return self.df

        # if user wants to save    
        if self.save == True:
           # save to file given user input
           self.df.to_csv(self.savepath, index=False) 
           return self.df