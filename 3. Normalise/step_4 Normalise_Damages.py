# -*- coding: utf-8 -*-
"""
This code merges the World Bank GDP data and the disaster dataframe. fater the merge it uses the 2019 GDP
to normalise the damages_USD
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import os

readfile = pd.read_excel(r'/Users/giotemp/Desktop/Cconsecutive Disasters Thesis/GDP.xlsx')
readfile.to_csv('gdp.csv')

folder_name = r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/Nomalise data/Census_Data'
file_name = r'gdp.csv'

file_path = os.path.join(folder_name, file_name)
data = pd.read_csv(file_path)

data1 = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/Nomalise data/Process/all_disaster_data_deaths_normalised.csv')
data_merged = data.merge(data1, on='Year', how= 'outer')

data_merged['damage_USD'] = data_merged['damage_USD'].astype(str).astype(float)
data_merged['n_damage_USD'] = 3.76796e+11/data_merged['GDP (current US$)'] * data_merged['damage_USD']

data_merged.to_csv('ndamages_ndeaths_1980-2018.csv')
