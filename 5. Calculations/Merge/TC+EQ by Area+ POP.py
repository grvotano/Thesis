#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code merges the tropical cyclone and earthquake impact data that has been redistirbuted by hazard and population overlap, there may be many entries\
    that were not redistributed as a resylt of matching hazard and impact dates but
    no spatial overlap of recorded entries in impact data with that of the hazard data.
    The initial code makes entries zero if the hazard is not overlapping with entries.
    Another possible way is to redistirbute by population distribution if dates match 
    without hazard overlap 
Created on Fri Apr  2 11:02:04 2021

@author: giovannivotano
"""

import pandas as pd

tc = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Redistributed /prep/TC_R_A+P_impacts.csv')
eq = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Redistributed /prep/EQ_R_A+P_impacts.csv')

frames = [tc, eq]
data = pd.concat(frames)
data = data[['NAME_1',"Year",'GID_1_2', 'disaster','began', 'ended','normalised', 'n_damage_U','R_Deaths', 'R_Damages' ]]

for i in range(len(data['disaster'])):
    if data.iloc[i].disaster == 'Flood':
        data.loc[i, 'disaster'] = 'Tropical Cyclone'
data['month'] = pd.to_datetime(data['began']).dt.to_period('M')      
data['began'] = pd.to_datetime(data['began'])
data.to_csv(r'Disaster_AP_Total.csv')


