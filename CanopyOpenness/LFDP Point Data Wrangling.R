####---ADDING COORDINATES FOR LFDP 40 POINT CANOPY HEMISPHERIC PHOTOS-----####

# Roí A.K., April 2021
# Columbia University, NY, NY

# Images in sample_photos folder for LFDP 40 points were processed using CanopyOpenness package in python
#   https://github.com/Roiak2/Canopy-Openness-from-Hemispheric-Photos 

# Once all years (2011, 2012, 2017) for the available photos were analyzed to get canopy openness,
#   They were output in one data file

####----------------------------THIS SCRIPT-------------------------------####

# This script takes that data file and adds to it the coordinates for each
#   photo within the LFDP

# It also creates a year and month column from the date column for easier 
#   future analyses



####--------------------------Packages and Data---------------------------####

#data manipulation library
library(tidyverse)
#where files are
local_path <- paste0(getwd(),"/Data/")

#loading openness data
open <- read_csv(paste0(local_path,"LFDP_40_Points.csv"))
#loading coordinate data
coord <- read_csv(paste0(local_path,"Coords_40_Points.csv"))


####--------------------------Adding Coordinates--------------------------####

#merging two data files based on subplot (i.e. one of the 40 points)
merged_d <- left_join(open,coord, by="Subplot")

####---------------------Creating Year and Month Columns------------------####

#Fixing datetime columns and adding month and year for easier analysis
merged_d <- merged_d %>%
  mutate(Date = lubridate::dmy(merged_d$Date),#turning date into a day, month, year column using lubridate
         Year = lubridate::year(Date), # adding separate columns for year and month
         Month = lubridate::month(Date)) %>%
  relocate(Plot,Subplot,Date,Year,Month,X,Y,Exposure,Openness)

#checking
str(open$Date) #Old data still as character
str(merged_d$Date) #merged data as date


####------------------------------Saving Data-----------------------------####

#Writing table to file
write_csv(merged_d, paste0(local_path,"LFDP_40_PointsFull.csv"))

