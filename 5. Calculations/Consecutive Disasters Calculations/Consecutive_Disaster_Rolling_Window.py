#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:21:35 2021
consecutive disasters = 915 (count by 30 day rolling window)
@author: giovannivotano
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/8.Consecutive Disasters/disasters_final.csv')
data['began'] = pd.to_datetime(data['began'])
sns.set_theme(style="darkgrid")
# Plot the responses for different events and regions
sns.lineplot(x="month", y="R_Deaths",  data=data)

# 30 day consecutive events 

time_window = 30
data
for window in data.groupby('Province'):
    print(window)



group = data.groupby('Province')
Agus_del_norte = group.get_group('Agusan del Norte')
abra.rolling('30d', on = 'began').sum()

# count number of consecutive disasters and sum()
disasters_sum = data.groupby('Province').rolling("30d", on ='began').sum()
disasters_sum.reset_index(inplace= True)
disasters_count = data.groupby('Province').rolling("30d", on ='began').count()

# create an index of diasters that have a value greater than one
disasters_index= disasters_count[disasters_count['month']> 1]
# select consecutive disaster entries using the created index
consecutive disasters = disasters_sum[disasters_sum['level_1']==(disasters_index['level_1'])]

