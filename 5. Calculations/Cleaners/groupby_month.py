#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 15:46:32 2021

@author: giovannivotano
"""

import pandas as pd

df = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/3.Normalised Data/normalised_data.csv')
df['month'] = pd.to_datetime(df['began']).dt.to_period('M')
df_dis = df.groupby('month')
df_dis = df.groupby('NAME_1').filter(lambda x: len(x) > 1)


if date in range(len(df['month'])):
    if df.iloc[date].

stats.to_csv(r'consecutive_disasters_sum_per_month.csv')
