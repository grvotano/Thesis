#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 16:04:53 2021

@author: giovannivotano
"""

import pandas as pd

data = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Tropical Cyclone/RISK_MAP/Impacts_with_R_class.csv')

data['began'] = pd.to_datetime(data[('began')]).dt.strftime('%Y-%m-%d')
dates = data['began'].unique()
pop = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/6. Population Manipulation/Population Density per Province.csv')
data = data.merge(pop, left_on='GID_1_2', right_on='GID_1')

# This part of the code creates nested arrays that contain 1. the date and 2. an array of classes
# noted on that date : ([date,[classes]])
date_h =[]

for date in dates:
    classes = []
    pop = []
    for i in range(len(data['began'])):
        if data.iloc[i].began == date:
            classes.append(data.loc[i,'class'])
            pop.append(data.loc[i,'Sumsum'])
            
    date_h.append([date, classes, pop])

# this next loop aggregates the classes in the array given per date
# intial = (2000-01-01, [1,1,1]) final = (2000-01-01, [3])
aggregate = []
for i, x, j in date_h:
    aggregate.append([i, sum(x), sum(j)])

data["total_h"] = ''

# this loop uses the date and aggregated value stored in the arrays to append
# the aggregate value per date to a new column in the flood impact data set 
for i, x, j in aggregate:
    for date in range(len(data['began'])):
        if data.loc[date, 'began'] == i:
            data.loc[date, 'total_h'] = x
            data.loc[date, 'total_pop'] = j

# creates a ratio using the class value over the total classes aggregate 
# and the ratio is applied to the impact data
rename = {'n_damage_U': 'N_D_USD', 'normalised':'N_Deaths' }
data.rename(columns= rename, inplace = True)
data['total_h'] = pd.to_numeric(data['total_h']) #.astype(str).astype(int)
data['R_Deaths'] = data['N_Deaths'] * (((data['class']/data['total_h']) + (data['Sumsum']/data['total_pop']))/2)
data['R_Damages'] = data['N_D_USD'] * (((data['class']/data['total_h']) + (data['Sumsum']/data['total_pop']))/2)

# export to csv
data_clean = data[['NAME_1_x',"Year",'GID_1_2', 'disaster','began', 'ended','N_Deaths', 'N_D_USD','R_Deaths', 'R_Damages' ]]
data.to_csv(r'TC_Impacts_HRPop.csv')
data_clean.to_csv(r'TC_CLean_Impacts_HRPop.csv')



