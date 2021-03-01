#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code import a dataframe containing total population values for each study year
in the Philippines and merges it with the existing disaster dataframe for 1980-2020

Created on Wed Jan 27 19:17:39 2021

@author: giovanniremovotano
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

read_file = pd.read_excel(r'/Users/giovanniremovotano/OneDrive - UvA/OneDrive - UvA/Philippines_Consecutive_Disasters_and_Migration_master/DATA/RAW/Total Populations Philippines 1980 - 2020.xls')
read_file.to_csv('Population_Philippines_1980_2020.csv')

foldername = r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/Nomalise data/Census_Data'
filename = r'Population_Philippines_1980_2020.csv'

filepath = os.path.join(foldername, filename)
data1 = pd.read_csv(filepath)

# manually remove the commas in entry # 40 and then continue 
data1['Total Population'] = pd.to_numeric(data1['Total Population'])

foldername = r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/Merge To GADM (geo-reference)/MASTER/csv'
filename = r'Master_for_Normalisation.csv'

filepath = os.path.join(foldername, filename)
data = pd.read_csv(filepath)

# create year column that is complete based on date 'began'
# first convert 'began' to datetime
data['began'] = pd.to_datetime(data['began'],  errors='coerce')
#add new column and extract year from 'began'
data['Year'] = data['began'].dt.year 
# merge data and population dataframe 

df = data.merge(data1, on = 'Year', how = 'outer')

df.drop('Total Population', axis= 1, inplace= True)
df.drop('Total Population', axis= 1, inplace= True)

df.to_csv('disaster_data_population_ready_to_normalise_deaths.csv')
  
  