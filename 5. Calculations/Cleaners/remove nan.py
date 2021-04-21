#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code removes entries where deaths and damages =  nan and 0 values 
Created on Fri Mar 26 10:24:03 2021

@author: giovannivotano
"""

import pandas as pd

data = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/3.Normalised Data/No_Duplicates.csv')
data['began'] = pd.to_datetime(data['began'])

data = data.dropna(subset=['normalised', 'n_damage_U'], how='all')

data = data[(data[['normalised', 'n_damage_U']] != 0).all(axis=1)]
group = data.groupby('NAME_1').sum('n_damage_U')
data.index = pd.to_datetime(data['began'])
group.to_csv(r'aggregate_by_province.csv')
data.to_csv(r'normalised_data.csv')