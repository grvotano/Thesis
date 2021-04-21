#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 10:24:12 2021

@author: giovannivotano
"""

import pandas as pd

tc = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Redistributed /prep/TC_CLean_Impacts_HRPop.csv')
ls = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Redistributed /prep/LS_CLean_Impacts_HRPop.csv')
eq = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Redistributed /prep/EQ_CLean_Impacts_HRPop.csv')
fl = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Redistributed /prep/FL_CLean_Impacts_HRPop.csv')
       

frames = [tc, ls, eq, fl]
data = pd.concat(frames)
data['month'] = pd.to_datetime(data['began']).dt.to_period('M')

# export 
data.to_csv(r'Disasters_RM_Total.csv')
