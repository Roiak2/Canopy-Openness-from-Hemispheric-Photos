## Paired Programming (smau8)

### Goal of the project: 
**Is it clear to you from the proposal.md how the goal can be accomplished using Python and the specified packages?**
Proposal.md explains the design and goal of the package well--a program that processes canopy fish-eye photos to quantify canopy openess and assess the impact of natural disasters on forests. The canopy openess package will mainly rely on using `scikit-image` to process and standardize all images for analyses. `scikit-image` will help 1) distinguish between the sky/canopy in each image using the blue channel, 2) convert images to black-and-white photos and 3) determine the circular border for each fish-eye image in preparation for statistical analysis with `numpy` (to quantify area of canopy vs. sky). 


### The Data: 
**Is it clear to you from the proposal.md what the data for this project is, or will look like?**
The data featured in this project is clearly stated in the proposal and the data featured will be canopy fish-eye images. The user will provide their own images for processing via this package. After image processing, the package will compute and produce a "Canopy-Openness metric" as a fraction on a scale of 0 to 1. The result is summarized and outputted in `.csv` format. Proposal.md also features sample images at different stages of image processing.


### The code: 
**(Look at the Python code files in detail first and try to comprehend a bit of what is written so far)
Does the current code include a proper skeleton (pseudocode) for starting this project?
What can this code do so far?
Given the project description, what are some individual functions that could be written to accomplish parts of this goal?**
All Python code is currently found in `CanOpen.py` and features the following class objects and functions, which provide a clear skeleton/pseudocode for the project with a methodical approach. An overview of the existing package structure is provided below. The current code is able to handle and prepare images provided by user input by first processing photos with the blue channel and then converting them into black/white images. The current code can also calculate the circle coordinates and the circle radius needed to determine the border of each fish-eye photo. The current code accomplishes roughly half of what the package intends as its goal and the remainder of the code is under development. The code has provided a comprehensive list of functions needed to accomplish the goal, and it will be beneficial to group these functions into class objects next.

Current code overview:
1. Image processing with class object `ImagePrep`
- Function #1: imageLoad = initial processing of image (user input)
- Function #2: BluePic = process image with blue channel to distinguish between sky vs canopy
- Function #3: bwPic = process blue channel image and convert it into black-and-white image
2. Determine circular boundaries of fish-eye image with class object `FishEye`
- Function #1: CircleCoords = find center coordinate of fish-eye circle
- Function #2: SetCircle = set circle based on center coordinate and radius
- Function #3: DrawCircle = draw circular boundary onto photo based on calculations (in development)
3. Calculate canopy openness based on image data with class object `CanOpen` (in development)
- Function #1: GapFractions = calculate gap fraction (canopy vs. sky fraction) (in development)
- Function #2: Openness = calculate final Canopy Openness as a fractional value using gap fraction. (in development)


### Code contributions/ideas: 
Given that the current skeleton of the code provides a good outline of all the functions needed to accomplish the goal of this project, I provided suggestions on creating class objects to better organize the existing functions and the code in general. 

The following suggestions were made in `ImagePrep.py`, where the `ImagePrep` class object was created and a demo of how this class object works can be found in a Jupyter notebook named `paired-programming-demo.ipynb`:
1. Grouped the three functions related to image processing (`imageLoad`, `BluePic`, `bwPic`) under one class object named `ImagePrep()`. 
2. Added an `__init__` function for the class object using `self.___` statements, which allows these functions to interact with each other so that the current workflow within this class object is:
- User provides their own images as input for initial processing with `imageLoad`
- output of `imageLoad` = input of `BluePic`, imageLoad output is given to BluePic so that image is processed with a blue channel
- output of `BluePic` = input of `bwPic`, BluePic output is given to bwPic so that the image is finally processed and converted into a black/white image.
3. Comments were added in the code to provide further context.
4. Added an import statement for `rgb2gray`, which the original code needed as a dependency

Next steps:
1. Used empty strings as temporary placeholders for most of the `self.___` statements in the `__init__` object so far, but would suggest looking into better/more specific placeholders if possible.
2. The current class objects outputs a numpy array before it produces an image (related to how scikit-image is implemented in the code?) and the next step would involve eliminating this numpy array as an output so that users only get their processed image in the end. 
3. Creating the other two class objects `FishEye` and `CanOpen`