#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 11:41:45 2021

This code uses the aggregated earthquake hits per municipality and scores them from 1-5
The resulting scores are used to redistribute impact data based on the ratio
of aggregated scores per province hit over the total scores per disaster.
'R = I * Ptotalscore/Dtotalscore'
@author: giovannivotano
"""

import pandas as pd

# import data
eq_hits = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Earthquake/municipal_hits_per_province_eq.csv')
eq = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Earthquake/N_R/EQ_NR_impacts.csv')
pop = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/6. Population Manipulation/Population Density per Province.csv')

# merge
data = eq.merge(eq_hits, left_on='GID_1_2', right_on='GID_1').   # merge impact with hazard data
data = data.merge(pop, left_on='GID_1_2', right_on='GID_1') 
data['began'] = pd.to_datetime(data[('began')]).dt.strftime('%Y-%m-%d')
dates = data['began'].unique()  # create a list of unique disasters (identified by start date)
data['R_Class'] = '' # create empty column to place risk score

for i, row in data.iterrows():                # loop to assign risk score based on number of hits
    if data.loc[i, 'total'] >= 1 and data.loc[i, 'total'] <= 15:
        data.loc[i, 'R_Class'] = 1
    if data.loc[i, 'total'] >= 15 and data.loc[i, 'total'] <= 30:
        data.loc[i, 'R_Class'] = 2
    if data.loc[i, 'total'] >= 30 and data.loc[i, 'total'] <= 45:
        data.loc[i, 'R_Class'] = 3
    if data.loc[i, 'total'] >= 45 and data.loc[i, 'total'] <= 60:
        data.loc[i, 'R_Class'] = 4
    if data.loc[i, 'total'] >= 60 and data.loc[i, 'total'] <= 75:
        data.loc[i, 'R_Class'] = 5
        
data['R_Class'] = pd.to_numeric(data['R_Class']) # from string to int
data['Sumsum'] = pd.to_numeric(data['Sumsum'])


date_h =[]    # create list and loop to store lists of disaster date, risk score (class) and population density

for date in dates:
    classes = []
    #pop = []
    for i in range(len(data['began'])):
        if data.iloc[i].began == date:
            classes.append(data.loc[i,'R_Class'])
            #pop.append(data.loc[i,'Sumsum'])
            
    date_h.append([date, classes]) #, pop

# this next loop aggregates the classes in the array given per date
# intial = (2000-01-01, [1,1,1]) final = (2000-01-01, [3])
aggregate = []
for i, x in date_h:    # , j 
    aggregate.append([i, sum(x)]) # , sum(j)

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
data['R_Deaths'] = data['N_Deaths'] * (data['R_Class']/data['total_h'])
data['R_Damages'] = data['N_D_USD'] * (data['R_Class']/data['total_h'])

data_clean = data[['NAME_1_x',"Year",'GID_1_2', 'disaster','began', 'ended','N_Deaths', 'N_D_USD','R_Deaths', 'R_Damages' ]]
data.to_csv(r'EQ_Impacts_by_Hazard.csv')
data_clean.to_csv(r'EQ_CLean_Impacts_Hazard_Redistribute.csv')