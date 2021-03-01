#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This os written to clean the emdat 1980 to 2012 geocoded data set as accurately as possible to
streamline the manual processing of enrties to the provincial level
Created on Tue Dec  8 12:53:56 2020

@author: giovanniremovotano
"""

import os
import pandas as pd
from datetime import datetime
import datetime
import matplotlib.pyplot as plt

# define file path and read in data
foldername = r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/EMDAT/RAW DATA/EM-DAT_PHL'
filename = "disasters_locations_merged.csv"

full_path = os.path.join(foldername, filename)
data = pd.read_csv(full_path)

# drop rows with na values in the date column
data.dropna(axis=0, how = 'any', subset=['start_isodate'], inplace = True)

# for loop to drop rows with incomplete date etries (any dates with less than three values)
## create variable that saves the for loop
data['len_dates']=[len(x.split('-')) for x in data['start_isodate'].values]

## use where function to split str into three parts
data.where(data.len_dates == 3, inplace = True)

## drop na values in the newly created column 
data.dropna(axis=0, how = 'any', subset = ['len_dates'], inplace = True)

# create new column with converted date to datetime
data['start_date'] = pd.to_datetime(data['start_isodate'], format="%Y-%m-%d")
data['end_isodate'] = [x.rstrip() for x in data['end_isodate'].values]
data['end_date'] = pd.to_datetime(data['end_isodate'], format="%Y-%m-%d")

# select relevant columns + rename columns
data = data[['disaster_id', 'disaster_subtype', 'disaster_type', 'disaster_subgroup', 'year', 'start_date', 'end_date', 'country_name','place_name', 'latitude', 'longitude', 'no_killed', 'total_dam_usd' ]]
columns_rename = {'place_name': 'detailed_locations','disaster_subtype' : 'disaster', 'disaster_type': 'disaster_category', 'start_date': 'began', 'end_date': 'ended', 'country_name': 'country', 'no_killed': 'dead', 'total_dam_usd': 'damage_USD'}
#rename = {'place_name': 'detailed_locations'}
data = data.rename(columns= columns_rename)

for idx, row in data.iterrows():
    if  data.loc[idx,'disaster'] == 'Avalanche': 
        data.loc[idx,'disaster'] = 'Volcanic Eruption'
    if  data.loc[idx,'disaster'] == 'Rockfall': 
        data.loc[idx,'disaster'] = 'Landslide'
    if  data.loc[idx,'disaster'] == "Tropical cyclone": 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
    if data.loc[idx, 'disaster'] == 'Flash flood':
        data.loc[idx,'disaster'] = 'Flood'

for idx, row in data.iterrows():
    if  data.loc[idx,'disaster'] == 'Earthquake (ground shaking)':
        data.loc[idx,'disaster'] = 'Earthquake'
    if  data.loc[idx,'disaster'] == 'Storm surge/coastal flood': 
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'Volcanic eruption': 
        data.loc[idx,'disaster'] = 'Volcanic Eruption'
    if data.loc[idx, 'disaster'] == 'General flood':
        data.loc[idx, 'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'General flood': 
        data.loc[idx,'disaster'] = 'Flood'
    if data.loc[idx, 'disaster'] == 'nan' and data['disaster_category'] == 'Flood':
        data.loc[idx, 'disaster'] = 'Flood'

data.drop(data.loc[data['disaster']== 'Local storm'].index, inplace=True) 
data.drop(data.loc[data['disaster']== 'Viral Infectious Diseases'].index, inplace=True) 
data.drop(data.loc[data['disaster']== 'Bacterial Infectious Diseases'].index, inplace=True) 
data.drop(data.loc[data['disaster']== 'Forest fire'].index, inplace=True)
data.drop(data.loc[data['disaster']== 'Subsidence'].index, inplace=True)

'Northern Mindanao' 'Cordillera Administrative Region'
'Bicol'
'Western Visayas'
# downlaod new dataframe 
data.to_csv('1980_2010_final.csv')
 


# basic plotting 
plt.figure()
#plt.scatter(data2['year'], data2['disaster_type'], linewidth= 1)
plt.scatter(data2['start_date'], data2['disaster_type'], s=15, alpha=0.5, c=data2['no_killed'], vmin=0, vmax=300)
plt.colorbar(extend='max')