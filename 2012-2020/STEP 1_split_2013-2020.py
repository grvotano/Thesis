 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code splits the locations of events into new rows for geo referencing 
Note: for str.split I changed str.split(',') to str.split(r',\s*(?=[^)]*(?:\(|$))') to skip brackets
Created on Wed Jan 13 16:13:17 2021

@author: giovanniremovotano
"""

import os
import pandas as pd
from datetime import datetime
import datetime
import matplotlib.pyplot as plt

# define file path and read in data
foldername = r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/EMDAT/RAW DATA'
filename = "em_dat_2012_2020.csv"

full_path = os.path.join(foldername, filename)
data = pd.read_csv(full_path)

# seperate the locations following a comma into new rows for each region
# Reindex and repeat cols on len of split and reset index
df1 = data.reindex(data.index.repeat(data['Location'].fillna("").str.split(r',\s*(?=[^)]*(?:\(|$))').apply(len)))
df1 = df1.drop(['Location'],1)

# Splitting both cols
s = data['Location'].str.split(r',\s*(?=[^)]*(?:\(|$))', expand= True).stack().reset_index(level=1,drop=True)

# Now grouping the series and df using cumcount.
df1 = df1.set_index(df1.groupby(df1.index).cumcount(), append=True)
s = s.to_frame('Location').set_index(s.groupby(s.index).cumcount(), append=True)


# Joining the all of them together and reset index.
df1 = df1.join(s, how='outer').reset_index(level=[0,1],drop=True)

# write data to csv # Folder "2012-2020 process"
df1.to_csv('STEP1: 2012_2020_split_loc.csv')


