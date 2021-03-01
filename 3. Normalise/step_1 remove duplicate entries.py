 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code is written to remove disaster entries that occur more than once in the same province 
Created on Wed Jan 27 17:14:33 2021

@author: giovanniremovotano
"""

import pandas as pd
import os
import numpy as np 

foldername = r'/Users/giovanniremovotano/OneDrive - UvA/OneDrive - UvA/Philippines_Consecutive_Disasters_and_Migration_master/DATA/from gis/attribute files'
filename = r'merged data ready to remove duplicate entries.csv'

filepath = os.path.join(foldername, filename)
data = pd.read_csv(filepath)

#create new dataframe with unique rows and only the first row of duplicate rows 
df1 = data.reset_index().drop_duplicates(subset=['NAME_1','disasterno', 'began'], keep='first').set_index('index')


df1.to_csv('GIS merged data excluding duplicate entries') 
