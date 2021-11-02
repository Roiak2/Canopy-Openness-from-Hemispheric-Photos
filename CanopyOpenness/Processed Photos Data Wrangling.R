####--------------------DATA WRANGLING CANOPY OPENNESS--------------------####

# Roí A.K., October 2021
# Columbia University, NY, NY

####------------------------------OVERVIEW--------------------------------####

# Images in sample_photos folder for LFDP 40 points & canopy trimming experiment (CTE)
#   were processed using CanopyOpenness package in python:
#   https://github.com/Roiak2/Canopy-Openness-from-Hemispheric-Photos 

# Once all years of LFDP (2011, 2012, 2017) for the available photos 
#   were analyzed to get canopy openness they were output in one data file

# Same for the 2017 CTE data

# And also for seedling plot data for 2009, 2010, 2011, 2012, 
#   2014, 2015, 2018

####----------------------------THIS SCRIPT-------------------------------####

# This script takes that data file and adds to it the coordinates for each
#   photo within the LFDP

# It also creates a year and month column from the date column for easier 
#   future analyses

# It then takes processed photos for the 2017 CTE
#   and separates the "Subplot" column into treatment and subplot

# It then takes processed photos for the 2009-2018 seedling plots
#   and fixes the "Focus" column to have NAs where it says JPG
#   and creates a year and month column from the date column for easier 
#   future analyses


####--------------------------Packages and Data---------------------------####

#data manipulation library
library(tidyverse)
#where files are
local_path <- "C:/Users/roiak/Documents/Damage Project/Canopy Photo Processing/Data/"

#loading openness data for LFDP 40 points
lfdp <- read_csv(paste0(local_path,"LFDP_all.csv"))
lfdp_21 <- read_csv(paste0(local_path,"LFDP_2021_Preprocessed.csv"))
#loading coordinate data
coord <- read_csv(paste0(local_path,"Coords_40_Points.csv"))

#loading openness data for CTE
cte <- read_csv(paste0(local_path,"CTE_all.csv"))
cte_21 <- read_csv(paste0(local_path,"CTE_2021_Preprocessed.csv"))

#loading openness data for seedling plots
seed <- read_csv(paste0(local_path,"Seedlings_all.csv"),
                 col_types = cols(Date = col_character(),
                                  Focus = col_character()))

#loading openness data for seedling 2020 plots
seed20 <- read_csv(paste0(local_path,"Seedlings_2020_Preprocessed.csv"),
                 col_types = cols(Date = col_character(),
                                  Focus = col_character()))

#seedlings 2021 data
seed21 <- read_csv(paste0(local_path,"Seedlings_2021_Preprocessed.csv"),
                   col_types = cols(Date = col_character(),
                                    Focus = col_character()))


####------------------------------LFDP 40 POINTS---------------------------####

####---Adding Coordinates---####

#merging two data files based on subplot (i.e. one of the 40 points)
merged_d <- left_join(lfdp,coord, by="Subplot")

####---Creating Year and Month Columns---####

#Fixing datetime columns and adding month and year for easier analysis
merged_d <- merged_d %>%
  mutate(Plot = "LFDP", #making sure plots say lfdp
         Date = lubridate::dmy(merged_d$Date),#turning date into a day, month, year column using lubridate
         Year = lubridate::year(Date), # adding separate columns for year and month
         Month = lubridate::month(Date)) %>%
  relocate(Plot,Subplot,Date,Year,Month,X,Y,Exposure,Focus,Openness) %>% #organizing column order
  arrange(Plot,Subplot,Date) #arranging by date within each subplot

#checking
str(lfdp$Date) #Old data still as character
str(merged_d$Date) #merged data as date


####---Saving Data---####

#Writing table to file
write_csv(merged_d, paste0(local_path,"LFDP_40_PointsFull.csv"))

#cleaning
rm(merged_d,lfdp,coord)


#--2021 DATA--#

#merging two data files based on subplot (i.e. one of the 40 points)
merged_d <- left_join(lfdp_21,coord, by="Subplot")

####---Creating Year and Month Columns---####

#Fixing datetime columns and adding month and year for easier analysis
merged_d <- merged_d %>%
  mutate(Plot = "LFDP", #making sure plots say lfdp
         Date = lubridate::dmy(merged_d$Date),#turning date into a day, month, year column using lubridate
         Year = lubridate::year(Date), # adding separate columns for year and month
         Month = lubridate::month(Date)) %>%
  relocate(Plot,Subplot,Date,Year,Month,X,Y,Exposure,Focus,Openness) %>% #organizing column order
  arrange(Plot,Subplot,Date) #arranging by date within each subplot

#checking
str(lfdp_21$Date) #Old data still as character
str(merged_d$Date) #merged data as date


####---Saving Data---####

#Writing table to file
write_csv(merged_d, paste0(local_path,"LFDP_2021_40PointsFull.csv"))

#cleaning
rm(merged_d,lfdp,coord)


####-------------------------------------CTE-------------------------------####

####---Creating Year and Month Columns---####

#Fixing datetime columns and adding month and year for easier analysis
cte2 <- cte %>%
  mutate(Date = lubridate::dmy(cte$Date),#turning date into a day, month, year column using lubridate
         Year = lubridate::year(Date), # adding separate columns for year and month
         Month = lubridate::month(Date)) %>%
  relocate(Plot,Subplot,Date,Year,Month,Exposure,Focus,Openness) %>% #organizing column order
  arrange(Plot,Subplot,Date) #organizing by date within subplot

#checking
str(cte$Date) #old date as character
str(cte2$Date) #new data as date

####---Creating treatment and subplot columns---####

#separating the Subplot column into treatment and then subplot (i.e. location of photo)
cte2 <- cte2 %>%
  separate(Subplot, 
           sep = "-", 
           into = c("Treatment","Subplot"))
  
####---Saving Data---####

#writing table to file
write_csv(cte2, paste0(local_path,"CTE_Full.csv"))

#cleaning
rm(cte,cte2)


##--2021 DATA--##

####---Creating Year and Month Columns---####

#Fixing datetime columns and adding month and year for easier analysis
cte_21_2 <- cte_21 %>%
  mutate(Date = lubridate::dmy(cte_21$Date),#turning date into a day, month, year column using lubridate
         Year = lubridate::year(Date), # adding separate columns for year and month
         Month = lubridate::month(Date)) %>%
  relocate(Plot,Subplot,Date,Year,Month,Exposure,Focus,Openness) %>% #organizing column order
  arrange(Plot,Subplot,Date) #organizing by date within subplot

#checking
str(cte_21$Date) #old date as character
str(cte_21_2$Date) #new data as date

####---Creating treatment and subplot columns---####

#separating the Subplot column into treatment and then subplot (i.e. location of photo)
cte_21_2 <- cte_21_2 %>%
  separate(Subplot, 
           sep = "-", 
           into = c("Treatment","Subplot"))

####---Saving Data---####

#writing table to file
write_csv(cte_21_2, paste0(local_path,"CTE_2021_Full.csv"))

#cleaning
rm(cte_21_2,cte_21_2)

####----------------------------------SEEDLINGS----------------------------####

####---Creating Year and Month Columns---####

# since 2009 data only has year and no date,
#   separating 2009 data and then will re-merge with full data after cleaning

seed2009 <- seed %>%
  filter(Date == '2009') #filtering for only 2009

#turning into date format (day and month are incorrect but year is)
seed2009$Date <- as.Date(as.character(seed2009$Date), format= "%Y")

#checking
str(seed$Date) #old data character
str(seed2009$Date) #new data number

# Non2009 data

#Taking rows where dates are completely numeric 
numyears <- seed[6481:7559,] #filtering

#Parsing out year and month from the day from the numeric
numyears <- numyears %>%
  mutate(Date = str_replace(Date,"2010","-2010"), #adding hyphens
         Date = str_replace(Date,substr(Date,1,1), #finding break between day and month
                             paste0(substr(Date,1,1),"-"))) #adding hyphens

#Turning into month day year column
numyears <- numyears %>%
  mutate(Date = lubridate::mdy(numyears$Date))

#Taking rows where dates are correct
no2009 <- seed[1077:6480,]  

#Turning into day month year column
no2009 <- no2009 %>%
  mutate(Date = lubridate::dmy(no2009$Date))

#Joining all non-2009 data together again with correct formatting
seed2 <- rbind.data.frame(no2009,numyears)

str(seed2$Date)

#Joining together with 2009 data
seed3 <- rbind.data.frame(seed2009,seed2)

#Fixing datetime columns and adding month and year for easier analysis
seed3 <- seed3 %>%
  mutate(Year = lubridate::year(Date), # adding separate columns for year and month
         Month = lubridate::month(Date)) %>%
  mutate(Month = ifelse(Year==2009,
                        NA,
                        Month)) %>% #if the year is 2009, make sure month is NA, otherwise keep
  relocate(Plot,Subplot,Date,Year,Month,Exposure,Focus,Openness) %>% #organizing column order
  arrange(Plot,Subplot,Date) #arranging dates within subplots

#checking
str(seed$Date) #old data as character
str(seed3$Date) #new data as date
str(seed3$Year) #year column numeric
str(seed3$Month) #month column numeric

####---Fixing NAs for Focus Column---####

#Turning all rows that say 'JPG' in the 'Focus' column into NAs
seed3 <- seed3 %>%
  mutate(Focus = ifelse(Focus == "JPG",
                        NA,
                        Focus)) #if Focus is JPG, turn to NA, otherwise keep

####---Saving Data---####

#writing table to file
write_csv(seed3, paste0(local_path,"Seedlings_Full.csv"))

#cleaning
rm(list = ls())
gc()


####---2020 Data---####
#Turning into day month year column
seed20 <- seed20 %>%
  mutate(Date = lubridate::dmy(seed20$Date))


#Fixing datetime columns and adding month and year for easier analysis
seed20 <- seed20 %>%
  mutate(Year = lubridate::year(Date), # adding separate columns for year and month
         Month = lubridate::month(Date)) %>%
  relocate(Plot,Subplot,Date,Year,Month,Exposure,Focus,Openness) %>% #organizing column order
  arrange(Plot,Subplot,Date) #arranging dates within subplots


####---Saving Data---####

#writing table to file
write_csv(seed20, paste0(local_path,"Seedlings2020_Full.csv"))

#cleaning
rm(seed20)
gc()

####---2021 Data---####
#Turning into day month year column
seed21 <- seed21 %>%
  mutate(Date = lubridate::dmy(seed21$Date))


#Fixing datetime columns and adding month and year for easier analysis
seed21 <- seed21 %>%
  mutate(Year = lubridate::year(Date), # adding separate columns for year and month
         Month = lubridate::month(Date)) %>%
  relocate(Plot,Subplot,Date,Year,Month,Exposure,Focus,Openness) %>% #organizing column order
  arrange(Plot,Subplot,Date) #arranging dates within subplots


####---Saving Data---####

#writing table to file
write_csv(seed21, paste0(local_path,"Seedlings2021_Full.csv"))

#cleaning
rm(list = ls())
gc()
