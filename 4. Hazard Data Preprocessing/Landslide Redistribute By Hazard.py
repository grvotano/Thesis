#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 10:00:03 2021

@author: giovannivotano
"""

import pandas as pd

ls = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Landslide/Landslide_R_Impacts.csv')
pop = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/6. Population Manipulation/Population Density per Province.csv')
# merge
data = ls.merge(pop, left_on='GID_1_2', right_on='GID_1')
data['began'] = pd.to_datetime(data[('began')]).dt.strftime('%Y-%m-%d')
dates = data['began'].unique()



date_h =[]

for date in dates:
    classes = []
    #pop = []
    for i in range(len(data['began'])):
        if data.iloc[i].began == date:
            classes.append(data.loc[i,'Hazard Fre'])
            #pop.append(data.loc[i,'Sumsum'])
            
    date_h.append([date, classes, pop])

# this next loop aggregates the classes in the array given per date
# intial = (2000-01-01, [1,1,1]) final = (2000-01-01, [3])
aggregate = []
for i, x in date_h:
    aggregate.append([i, sum(x)])

data["total_h"] = ''

# this loop uses the date and aggregated value stored in the arrays to append
# the aggregate value per date to a new column in the flood impact data set 
for i, x in aggregate:
    for date in range(len(data['began'])):
        if data.loc[date, 'began'] == i:
            data.loc[date, 'total_h'] = x
            #data.loc[date, 'total_pop'] = j

# creates a ratio using the class value over the total classes aggregate 
# and the ratio is applied to the impact data
rename = {'n_damage_U': 'N_D_USD', 'normalised':'N_Deaths' }
data.rename(columns= rename, inplace = True)
data['R_Deaths'] = data['N_Deaths'] * (data['Hazard Fre']/data['total_h'])
data['R_Damages'] = data['N_D_USD'] * (data['Hazard Fre']/data['total_h'])

data_clean = data[['NAME_1_x',"Year",'GID_1_2', 'disaster','began', 'ended','N_Deaths', 'N_D_USD','R_Deaths', 'R_Damages' ]]
data.to_csv(r'LS_Impacts_Redistribute_By_Hazard.csv')
data_clean.to_csv(r'LS_CLean_Impacts_Redistribute_By_Population.csv')
