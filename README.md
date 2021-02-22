# Hack-the-planet-project

## Project pre-proposal outline for EEEB 4050, Spring 2021 (in development)
---

### Description of Project Goals:
This package will take input of hemispheric photos and output a dataframe and plots estimating light exposure for each photo and in bulk for many photos.

### Description of Code:
The program will contain many functions to calculate light exposure based on hemispheric photos:
   - Normalize light exposure from the input photo file (contrast and exposure)
   - Convert photo to black and white or greyscale
   - Calculate what is *sunlight* and what is *not sun* (white vs. black)
   - Calculate % light per area of photo
   - Plot results
   - Save light exposure results and photo information in a csv file  

### Description of Data:
**Inputs -** 
   - jpeg or png files of hemispheric photos
   - location, date, and/or other identifying information of each photo (either in csv file or in the photo file name)
**Outputs -** 
   - jpegs or png files of plots of light amount & photosynthetically active radiation (PAR)
   - csv file of light exposure per photo with columns identifying location/time of each photo

### Description of User Interface:

