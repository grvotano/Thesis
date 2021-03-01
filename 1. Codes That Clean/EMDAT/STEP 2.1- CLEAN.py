#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is part two of processing the emdat 2102 - 2020 data fro geocding in GIS
This code cleans and creates a uniform format for all dataframes to join
Manually change entries 340-350 in disaster col to "Tropical Cyclone"
    63-70 to "Volcanic Eruption"
    455-466 to "Tropical Cyclone" source: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjZtbSNj-TuAhWREBQKHZIbDJ8QFjAFegQIDBAC&url=https%3A%2F%2Fwww.bbc.com%2Fnews%2Fworld-asia-42464644&usg=AOvVaw1pClmoC9_Iwq3iRE9xdYP5
    467-472 to "Tropical Cyclone"
    246-274 leaving as nan to convert to flood
Converts disaster nan values to "Flood" 
Created on Fri Feb 12 10:22:18 2021

@author: giovannivotano
"""

## PART 2: CLEAN
import os
import pandas as pd
from datetime import datetime
import datetime
import matplotlib.pyplot as plt

# define file path and read in data
foldername = r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/EMDAT/PREP/2012-2020 process'
filename = "2012_2020_split_locations.csv"

full_path = os.path.join(foldername, filename)
data = pd.read_csv(full_path)

# select columns
data = data[['Dis No', 'Event Name', 'Entry Criteria', 'Country', 'Year', 'Disaster Type', 'Disaster Subgroup','Disaster Subtype', 'Disaster Subsubtype', 'Origin', 'Region', 'Location','Latitude', 'Longitude', 'Total Deaths', 'Start Year', 'Start Month', 'Start Day', 'End Year', 'End Month', 'End Day', 'damages_USD' ,"Total Damages ('000 US$)"]]

# convert to datetime, have to change the column names to macth the format for the date_time function 
## first apply to start date
datetime = {'Start Year': 'year', 'Start Month': 'month', 'Start Day': 'day'}
data = data.rename(columns= datetime)
data['start_date'] = pd.to_datetime(data[['day','month', 'year']])

## change names back
reverse_names = {'year': 'Start Year', 'month': 'Start Month', 'day': 'Start Day'}
data = data.rename(columns = reverse_names)

## apply to end date
datetime_end = {'End Year': 'year', 'End Month': 'month', 'End Day': 'day'}
data = data.rename(columns= datetime_end)
data['end_date'] = pd.to_datetime(data[['day','month', 'year']])

# select columns again
data = data[['Dis No', 'Country','Year', 'Disaster Type', 'Disaster Subgroup','Disaster Subtype', 'Event Name', 'Origin', 'Region', 'Location','Latitude', 'Longitude', 'Total Deaths', 'start_date', 'end_date', 'damages_USD']]

# rename columns to match master data set
columns_rename = {'Dis No': 'disasterno', 'Entry Criteria': 'entry_criteria' ,'Country': 'country', 'Year': 'year', 'Location': 'detailed_locations' , 'Origin': 'origin', 'Region':'region','Latitude': 'latitude', 'Longitude': 'longitude', 'Disaster Subtype': 'disaster', 'Disaster Subgroup' : 'disaster_subgroup', 'Disaster Type': 'disaster_category', 'Event Name': 'event_name', 'start_date': 'began', 'end_date': 'ended', 'country_name': 'country', 'Total Deaths': 'dead'}

data = data.rename(columns= columns_rename)

# shorten string length of disasterno field to cute out '-PHL' in order to match disaster locations shape file
data['disasterno'] = data['disasterno'].str.slice(0,9)

# for loop to clean disaster column 
# contains a line to convert nan to flood (based on data in other columns that suggest its flooding)
    
for idx, row in data.iterrows():
    if  data.loc[idx,'disaster'] == 'nan': 
        data.loc[idx,'disaster'] = 'Flood'
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
    if  data.loc[idx,'disaster'] == 'Ash fall': 
        data.loc[idx,'disaster'] = 'Volcanic Eruption'
    if  data.loc[idx,'disaster'] == 'Ground movement': 
        data.loc[idx,'disaster'] = 'Earthquake'
    if data.loc[idx, 'disaster'] == 'Riverine flood':
        data.loc[idx,'disaster'] = 'Flood'
    if  data.loc[idx,'disaster'] == 'Lava flow':
        data.loc[idx,'disaster'] = 'Volcanic Eruption'
    elif  data.loc[idx,'disaster'] == 'Tropical Storm "Basyang" (Conson)': 
        data.loc[idx,'disaster'] = 'Tropical Cyclone'
        
# drop hazards/ disasters not relevant to the analysis
data.drop(data.loc[data['disaster']== 'Air'].index, inplace=True)
data.drop(data.loc[data['disaster']== 'Explosion'].index, inplace=True)
data.drop(data.loc[data['disaster']== 'Road'].index, inplace=True)
data.drop(data.loc[data['disaster']== 'Fire'].index, inplace=True)
data.drop(data.loc[data['disaster']== 'Water'].index, inplace=True) 
data.drop(data.loc[data['disaster']== 'Rockfall'].index, inplace=True)
data.drop(data.loc[data['disaster']== 'Local storm'].index, inplace=True) 
data.drop(data.loc[data['disaster']== '21'].index, inplace=True)
data.drop(data.loc[data['disaster']== 'Viral Infectious Diseases'].index, inplace=True) 
data.drop(data.loc[data['disaster']== 'Bacterial Infectious Diseases'].index, inplace=True) 
data.drop(data.loc[data['disaster']== 'Forest fire'].index, inplace=True)
data.drop(data.loc[data['disaster']== 'Subsidence'].index, inplace=True)# drop hazards/ disasters not relevant to the analysis 
data.drop(data.loc[data['disaster']== 'Rockfall'].index, inplace=True)
data.drop(data.loc[data['disaster']== 'Local storm'].index, inplace=True) 
data.drop(data.loc[data['disaster']== '21'].index, inplace=True)
data.drop(data.loc[data['disaster']== 'Viral Infectious Diseases'].index, inplace=True) 
data.drop(data.loc[data['disaster']== 'Bacterial Infectious Diseases'].index, inplace=True) 
data.drop(data.loc[data['disaster']== 'Forest fire'].index, inplace=True)
data.drop(data.loc[data['disaster']== 'Subsidence'].index, inplace=True)

data.iloc[63,]


# convert column to str for plotting purposes 
data['disaster'] = data['disaster'].apply(str)

# write dataframe to csv # folder "2012 -2020 process"
data.to_csv('Step2: 2012-2020_CLEAN.csv')

plt.scatter(data['year'], data['disaster'], linewidth= 1)
plt.scatter(data['year'], data['disaster'], alpha=0.5, c=data['dead'], vmin=0, vmax=300)
plt.colorbar(extend='max')
