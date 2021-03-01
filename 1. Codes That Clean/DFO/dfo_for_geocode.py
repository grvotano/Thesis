Created on Sat Jan  2 11:55:37 2021 updated 11-2-2021
This is the complete preprocessing code to clean the DFO flood data for georeferencing in GIS 
or futher spatial resolution realignment for reference by merge with GADM areas
@author: giovanniremovotano

import os
import pandas as pd
from datetime import datetime
import datetime
import matplotlib.pyplot as plt

read_file = pd.read_excel(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/DFO/RAW DATA/MasterList (2).xls')
read_file.to_csv('dfo_master.csv')
# import data 
foldername = r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/DFO/RAW DATA'
filename = 'dfo_master.csv'

full_path = os.path.join(foldername, filename)
data = pd.read_csv(full_path)

rename_column = {'Country (click on active links to access current and past inundation extents)': 'country', 'Notes and Comments (may include quoted headlines from copyrighted news stories for internal research purposes only)': 'notes'}
data = data.rename(columns= rename_column)
# select only entreis for the Philippines 
data = data.loc[data['country'] == 'Philippines']

# change object to datetime
data['Began'] = pd.to_datetime(data['Began'])
data['Ended'] = pd.to_datetime(data['Ended'])

# reindex, change from decending to accending dates  
data = data.sort_values(by= "Began")
data = data.reset_index(drop= True)

# select only relevant columns 
data = data[['notes','country','Register #', 'Glide #' ,'Detailed Locations', 'Began', 'Ended', 'Duration in Days', 'Dead', 'Displaced', 'Damage (USD)', 'Main cause', 'Severity *', 'Affected sq km', 'Magnitude (M)**','Centroid X','Centroid Y', 'Date Began']]

# change column names to match em_dat dataset 
columns_rename = {'Detailed Locations' : 'detailed_locations','Register #': 'register_#', 'Began' : 'began', 'Ended' : 'ended', 'Duration in Days' : 'duration_in_days', 'Dead' : 'dead', 'Displaced': 'displaced', 'Damage (USD)' : 'damage_USD', 'Main cause' : 'disaster', 'Severity *' : 'severity*', 'Affected sq km': 'affected_sq_km', 'Magnitude (M)**': 'magnitude_M**','Centroid X': 'centroid_x','Centroid Y': 'centroid_y', 'Date Began': 'date_began'}
data = data.rename(columns = columns_rename)

# add column that calculates duration in days 
#data2['duration_in_days'] = data2['ended'] - data2['began']

# for loop to clean disaster column 
    
for idx, row in data.iterrows():
    if  data.loc[idx,'disaster'] == 'Tropical cyclone': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
    if data.loc[idx, 'disaster'] == 'Flash flood':
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'Earthquake (ground shaking)':
        data.loc[idx,'disaster'] = 'Earthquake'
    if  data.loc[idx,'disaster'] == 'Storm surge/coastal flood': 
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'Volcanic eruption': 
        data.loc[idx,'disaster'] = 'Volcanic Eruption'
    if  data.loc[idx,'disaster'] == 'Brief torrential rain': 
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'General flood': 
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'Heavy rain': 
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'Monsoonal rain': 
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'Monsoonal Rain': 
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'Avalanche': 
        data.loc[idx,'disaster'] = 'Landslide'
    if  data.loc[idx,'disaster'] == 'Typhoon Fenshen': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
    if  data.loc[idx,'disaster'] == 'Tropical Storm "Fung-wong"': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
    if  data.loc[idx,'disaster'] == 'Heavy Rain': 
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'Tropical Storm and Heavy Rain': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
    if  data.loc[idx,'disaster'] == 'Torrential Rain': 
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'Tropical Cyclone, Morakot': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
    if  data.loc[idx,'disaster'] == 'Tropical Storm': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
    if  data.loc[idx,'disaster'] == 'Tropical Storm Mirinae': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
    if  data.loc[idx,'disaster'] == 'Typhoon Parma': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
    if  data.loc[idx,'disaster'] == 'Tropical storm Ketsana/Ondoy': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
    if  data.loc[idx,'disaster'] == 'Tropical Cyclone  ': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
    if  data.loc[idx,'disaster'] == 'Rockfall': 
        data.loc[idx,'disaster'] = 'Landslide'
    if  data.loc[idx,'disaster'] == 'Riverine flood': 
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'Bacterial Infectious Diseases': 
        data.loc[idx,'disaster'] = 'Other'
    if  data.loc[idx,'disaster'] == 'Forest fire': 
        data.loc[idx,'disaster'] = 'Other'
    if  data.loc[idx,'disaster'] == 'Subsidence': 
        data.loc[idx,'disaster'] = 'Other'
    if  data.loc[idx,'disaster'] == 'Viral Infectious Diseases': 
        data.loc[idx,'disaster'] = 'Other'
    if  data.loc[idx,'disaster'] == '21': 
        data.loc[idx,'disaster'] = 'Other'
    if  data.loc[idx,'disaster'] == 'Ground movement':
        data.loc[idx,'disaster'] = 'Earthquake'
    if  data.loc[idx,'disaster'] == 'Lava flow':
        data.loc[idx,'disaster'] = 'Volcanic Eruption'
    elif  data.loc[idx,'disaster'] == 'Tropical Storm "Basyang" (Conson)': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'

# seperate the locations following a comma into new rows for each region
# Reindex and repeat cols on len of split and reset index
df1 = data.reindex(data.index.repeat(data['detailed_locations'].fillna("").str.split(r',\s*(?=[^)]*(?:\(|$))').apply(len)))
df1 = df1.drop(['detailed_locations'],1)

# Splitting both cols
s = data['detailed_locations'].str.split(r',\s*(?=[^)]*(?:\(|$))', expand= True).stack().reset_index(level=1,drop=True)
  
# Now grouping the series and df using cumcount.
df1 = df1.set_index(df1.groupby(df1.index).cumcount(), append=True)
s = s.to_frame('detailed_locations').set_index(s.groupby(s.index).cumcount(), append=True)


# Joining the all of them together and reset index.
df1 = df1.join(s, how='outer').reset_index(level=[0,1],drop=True)


# write data to excel 
#df1.to_csv('emdat_2012_2020_split_locations.csv')
# export dataset folder: "DATA_BASE/DFO/READY FOR GEO_REFERENCE"
df1.to_csv('dfo_ready.csv')
