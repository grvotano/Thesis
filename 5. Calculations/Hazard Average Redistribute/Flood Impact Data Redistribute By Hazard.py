#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code takes the risk classes of each province per disaster, aggregates the classes per event 
and creates a ratio (class per province per event/ total classes(combined provinces affected) per event )
This ratio is then used to redistribute the impact data more accurately per province per entry
Created on Fri Feb 26 14:08:19 2021

@author: giovannivotano
"""

import pandas as pd
from collections import Counter 
import geopandas as gpd

fl_risk = gpd.read_file(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/Spatial _Data/phl_ica_floodrisk_geonode_mar2014/phl_ica_floodrisk_geonode_mar2014.shp')
flood = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Flood/CSV/NR/NR_fl.csv')
flood['began'] = pd.to_datetime(flood[('began')]).dt.strftime('%Y-%m-%d')
dates = flood['began'].unique()
pop = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/6. Population Manipulation/Population Density per Province.csv')

# add flood class per province by merging flood risk data with flood impact data
flood = flood.merge(fl_risk, how='inner', left_on='NAME_1', right_on='adm2_name').drop(columns= 'geometry')
flood = flood.merge(pop, left_on='GID_1_2', right_on='GID_1')
# This part of the code creates nested arrays that contain 1. the date and 2. an array of classes
# noted on that date : ([date,[classes]])
date_h =[]

for date in dates:
    classes = []
    pop = []
    for i in range(len(flood['began'])):
        if flood.iloc[i].began == date:
            classes.append(flood.loc[i,'FloodClass'])
            #pop.append(flood.loc[i,'Sumsum'])
    date_h.append([date, classes])

# this next loop aggregates the classes in the array given per date
# intial = (2000-01-01, [1,1,1]) final = (2000-01-01, [3])
aggregate = []
for i, x in date_h:
    aggregate.append([i, sum(x)])

flood["total_h"] = ''

# this loop uses the date and aggregated value stored in the arrays to append
# the aggregate value per date to a new column in the flood impact data set 
for i, x in aggregate:
    for date in range(len(flood['began'])):
        if flood.loc[date, 'began'] == i:
            flood.loc[date, 'total_h'] = x
            #flood.loc[date, 'total_pop'] = j

# creates a ratio using the class value over the total classes aggregate 
# and the ratio is applied to the impact data
rename = {'n_damage_U': 'N_D_USD', 'normalised':'N_Deaths' }
flood.rename(columns= rename, inplace = True)
flood['R_Deaths'] = flood['N_Deaths'] * (flood['FloodClass']/flood['total_h'])
flood['R_Damages'] = flood['N_D_USD'] * (flood['FloodClass']/flood['total_h'])
data = flood
# export to csv
data_clean = data[['NAME_1_x',"Year",'GID_1_2', 'disaster','began', 'ended','N_Deaths', 'N_D_USD','R_Deaths', 'R_Damages' ]]
data.to_csv(r'FL_Impacts_Redistribute_By_Hazard.csv')
data_clean.to_csv(r'FL_CLean_Impacts_Redistribute_By_Hazard.csv')




