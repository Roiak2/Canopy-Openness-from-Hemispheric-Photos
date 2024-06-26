# Canopy Openness from Hemispheric Photos

Canopy openness - the amount of light penetrating a canopy - is a crucial metric in understanding ecosystem dynamics and function, especially after a disturbance like a fire or a cyclone.

This package assists foresters by taking an input of hemispheric photos, calculating canopy openness for the photos, and outputting a dataframe with the results, as well as pretty plots.

<p align="center"><img src="/sample_photos/Sample_Photo.JPG" height="500">

<p align="center"><img src="/sample_photos/Sample_Photo_Threshold.jpg" height="500">

This package is inspired by Hans ter Steege (2018) Hemiphot.R: Free R scripts to analyse hemispherical 
photographs for canopy openness, leaf area index and photosynthetic active radiation under forest canopies.  
Unpublished report. Naturalis Biodiversity Center, Leiden, The Netherlands, https://github.com/Hans-ter-Steege/Hemiphot

The updates of this package to Hans ter Steege's are:
    - This is in python and therefore accessible to others who don't use R
    - This package uses thresholding algorithms instead of manually thresholding images to more objectively calculate openness in batch mode

### In Development

This program can be installed this way:

```
#install dependency pacakages
conda install pandas matplotlib numpy natsort scikit-image -c conda-forge 

#clone repository of package
git clone [https://github.com/Roiak2/Canopy-Openness-from-Hemispheric-Photos]

#enter into the cloned directory
cd ./Canopy-Openness-from-Hemispheric-Photos

#install onto your machine
pip install -e .
```

### Working example

After loading the program in your machine, you can go to the `WorkingExample.ipynb` and `Batch_Test.ipynb` jupyter notebooks found in the top directory of this repo. Do this by running this code after making sure to cd into the repo on your machine:

```
jupyter notebook .

```

These notebooks contain two sample workflows for you to test the ImageLoad, FishEye, and CanopyOpenness modules with a single sample photo or batch processing of all images in a given directory (you can try it on your own pictures as well).

As the package gets developed, the working example notebook will be updated to reflect developments.

