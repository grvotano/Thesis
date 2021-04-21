#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code aggregates the total earthquake hits per municipality
Created on Fri Mar 19 11:31:40 2021

@author: giovannivotano
"""

import math
import pandas as pd
import numpy as np
import geopandas as gpd
import fiona
import json
import matplotlib.pyplot as plt

# data
municipalities = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/4.Hazard Data/TC/Redistribution/Municipal_Areas.csv')
eq = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/4.Hazard Data/EQ/eq_buffer.csv')
#disaster = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/4.Hazard Data/TC/Redistribution/TC_Impacts.csv')


# clean
rename = {'Unnamed: 0': 'Municipalities'}
eq = eq.rename(columns=rename)

# count entries per mun (row) that contain a str. value
for i in range(len(eq['Municipalities'])):
    eq['total']= np.sum(eq.applymap(lambda x: 1 if isinstance(x, str) else 0), axis=1) -1

# select only relevant columns + merge provincial names to municipal data
eq = eq[['Municipalities','total']]
eq = eq.merge(municipalities, left_on='Municipalities', right_on='GID_2', how='inner')
eq = eq[['Municipalities', 'GID_1', 'GID_2', 'total']]

# sum total frequency of municipal hits per province
eq_hits_per_prov = eq.groupby(['GID_1'], as_index=False)['total'].sum()

eq_hits_per_prov.to_csv(r'municipal_hits_per_province_eq.csv')

