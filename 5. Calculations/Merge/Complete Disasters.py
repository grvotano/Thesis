#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 11:14:51 2021

@author: giovannivotano
"""

import pandas as pd

HM = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/7. Merge/Disasters_RM_Total.csv')
AP = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/7. Merge/Disaster_AP_Total.csv')

frames = [HM, AP]
data = pd.concat(frames)
data.to_csv(r'Complete_Disasters.csv')
