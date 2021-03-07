# Canopy Openness from Hemispheric Photos

## Project proposal outline for EEEB 4050, Spring 2021 (in development)
---

### Description of Project Goal:
Canopy openness - the amount of light penetrating a canopy - is a crucial metric in understanding ecosystem dynamics and function, especially after a disturbance like a fire or a cyclone.

This package assists foresters by taking an input of hemispheric photos, calculating canopy openness for the photos, and outputting a dataframe with the results, as well as pretty plots.

### User Input and Interface
The program requires the user to input image files. These will be jpeg or png files and should be fisheye photos.

For example:

<img src="Sample Photos/Sample_Photo.JPG height="100">

The photo is then loaded and saved to be manipulated. This can be easily achieved once the program is loaded into a notebook/script/command line. 

An example below:

```
#import program
import CanOpen

#load single image
image = CanOpen.load_image("./images/[image name].jpg)

#alternatively, can load batch images from single directory
batch_images = CanOpen.list_files("images/",pattern = ".JPEG")

#then program will load images in a for loop as for a single image

```

Therefore this program uses a Python API so users can interactively tweak and view results to fit their preferred use.

### Description of Data:
**Inputs -** 
   - jpeg or png files of hemispheric photos
   - location, date, and/or other identifying information of each photo (either in csv file or in the photo file name)  

**Outputs -** 
   - jpegs or png files of plots of canopy openness
   - csv file of openness per photo with columns identifying location/time of each photo

A csv output example:

| Photo | lon | Month | Canopy_Openness |
|-------|-----|-------|-----------------|
| 1A    | 73.4| May   | 64.5            |

A photo example showing black and white for canopy vs. sky:

<img src="Sample Photos/Sample_Photo_Threshold.JPG height="100">

**Output locations -**
The user will be able to save the resultant csv and plots into a directory of their choosing, whether in a remote server or on their own machine by choosing a filepath.

This program design and output type is following ter Steege, Han (2021) at the *Naturalis Biodiversity Center, Leiden, The Netherlands*

### Description of Code:
The program will contain a module with a few different class types to calculate canopy openness from hemispheric photos and output them as csv (for more detail please see CanOpen.py in the CanOpenness folder):
   - Class to load and prepare images from user:
     - Using scikit-image package, will load image
     - Convert image to our format, by using image dimensions to locate center of circle and border
     - Choose blue channel from RGB to highlight difference between sky and canopy
     - Convert to binary black and white canopy vs. sky (how to pick threshold?)
   - Class to calculate what is *sunlight* and what is *not sun* (white vs. black)
     - Break image into smaller spheres, calculate area of sunlight in each
     - Add all fraction calculations and divide by total area of photo to give canopy openness value
   - Class to plot images
     - Takes input from raw image, image converted to blue channel, or image converted to black and white, and plot it using toyplot 
   - Class to save outputs
     - Iterate through image files in a given directory to calculate canopy openness, store the result in csv
     - Given user input filepath save csv to given filepath
     - Option to save plots as image files in a given directory
