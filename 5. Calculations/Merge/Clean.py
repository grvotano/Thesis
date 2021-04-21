#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 14:22:10 2021

@author: giovannivotano
"""

import pandas as pd

# import data
data = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/7. Merge/Complete_Disasters.csv')

# clean data
data = data.reset_index()
columns = ['index', 'Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1']
data.drop(columns=columns, inplace=True)
rename = {'NAME_1_x': 'Province', 'NAME_1': 'Province', 'normalised': 'N_Deaths', 'n_damage_U': 'N_D_USD'}
data.rename(columns=rename, inplace=True)

# join columns with same name
def sjoin(x): return ';'.join(x[x.notnull()].astype(str))
data = data.groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1))

# drop rows where detahs and damages are 0 or Nan
data.dropna(subset=['R_Deaths','R_Damages'], how= 'all', inplace = True)
data.where((data['R_Deaths'] == NaN) & (data['R_Damages'] == NaN)).drop(index, axis= 0)

# export data frame
data.to_csv(r'Disasters_Cleaned.csv')
