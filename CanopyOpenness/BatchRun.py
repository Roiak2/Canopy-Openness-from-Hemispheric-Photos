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

