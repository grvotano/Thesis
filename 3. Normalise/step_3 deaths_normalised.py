#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code normalises the deaths by disasters in the philippines with the populationof 2020
Created on Thu Jan 28 13:19:00 2021

@author: giovanniremovotano
"""
import pandas as pd
import numpy as np
import os

foldername = r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/Nomalise data/Process'
file_name= r'disaster_data_population_ready_to_normalise_deaths.csv'

file_path = os.path.join(foldername, file_name)
data = pd.read_csv(file_path)

data['normalised_deaths'] = 108116615/ data['Total Population'] * data['dead']

# export to database/normalise/process
data.to_csv('all_disaster_data_deaths_normalised.csv')
