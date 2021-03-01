#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean the TC + Buffer data given by Marleen and Anaïs.
    FOR TC file select only columns that contain the PHL
    Drop all rows that only have nan values (removes entries from previous countries that no longer have columns)
  Exports a dataframe that is used as the hazard data in the code that redistributes impact
  data based on an overlap
Created on Mon Mar  1 18:49:06 2021

@author: giovannivotano
"""

import pandas as pd
import fiona
import geopandas as gpd
import matplotlib.pyplot as plt
import descartes
import json
import numpy as np

# read in area shp file and EQ json data-frame
data = pd.read_json(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/Spatial _Data/EQ + TC +BUFFER/EQ_admin2_1960_2016.geojson.json')

# create new data-frame selecting only Philippines (PHL) columns from json dataframe 
data =  data.loc[:, data.columns.str.startswith('PHL')]
data.dropna(axis=0, how='all', inplace= True)

# convert index of data to datetime
data['date'] = data.index
data.set_index('date', inplace= True)
# index in ascending order 
# at this point, the dataframe allows you to access all areas hit on a given date
data = data.sort_index(ascending= True)

# switch the axis of the EQ  
# This bit of code exports a csv containing the GADM L2 names as index and date (date_time) columns of EQ events 
# The exported file can be uploaded in GIS and joined by attribute to the GADM areas shape file 
data_new = data.T
data_new.to_csv('TC_buffer.csv')