#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:35:19 2021

@author: giovanniremovotano
"""

import os
import pandas as pd
from datetime import datetime
import datetime
import matplotlib.pyplot as plt

# convert xlsx to csv
read_file = pd.read_excel (r'/Users/giovanniremovotano/OneDrive - UvA/OneDrive - UvA/Philippines_Consecutive_Disasters_and_Migration_master/DATA/RAW/Philippines_Quakes_James.xlsx')
read_file.to_csv (r'/Users/giovanniremovotano/OneDrive - UvA/OneDrive - UvA/Philippines_Consecutive_Disasters_and_Migration_master/DATA/RAW/Philippines_Quakes_James.csv', index = None, header=True)

#import data
foldername = r'/Users/giovanniremovotano/OneDrive - UvA/OneDrive - UvA/Philippines_Consecutive_Disasters_and_Migration_master/DATA/RAW'
filename = 'Philippines_Quakes_James.csv'
fullpath = os.path.join(foldername, filename)
data = pd.read_csv(fullpath)

# convert to datetime 
# have to change the column names to macth the format for the date_time function 
datetime = {'Day_start': 'day', 'Month_start' : 'month', 'Year_start' : 'year'}
data= data.rename(columns= datetime)
data['start_date'] = pd.to_datetime(data[['day','month', 'year']])

# select columns 
data = data[['Event_type','ISO Country', 'EQ_Latitude', 'EQ_Longitude', 'EQ_Magnitude', 'EQ_Mag_Src', 'EQ_depth', '.Deaths', 'start_date', 'Econ_Loss_US', 'Econ_Loss_US_Upper', 'Econ_Loss_US_Lower']]

# change column names to match master dataset 
rename = {'Event_type': 'disaster','ISO Country': 'country', 'EQ_Latitude': 'latitude', 'EQ_Longitude': 'longitude','.Deaths': 'dead', 'start_date': 'began', 'Econ_Loss_US': 'damage_USD'}
data = data.rename(columns= rename)

# export dataset
data.to_csv('james_earthquake.csv')
