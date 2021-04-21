#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 11:15:37 2021
This code explodes the disaster dataframe to have start date to end date as index for entire 
period of study 
@author: giovannivotano
"""

import pandas as pd

impact_data = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/8.Consecutive Disasters/disasters_final.csv')

# explode entries over start and end date for full period of event
impact_data['Date'] = [pd.date_range(s, e, freq='d') for s, e in      # date range between start and end date 
              zip(pd.to_datetime(impact_data['began']), pd.to_datetime(impact_data['ended']))]
impact_data = impact_data.explode('Date').drop(['began', 'ended'], axis=1) # explodes entries for time period of each event

date_range = pd.date_range(start= '1980-07-25', end = '2019-12-28', freq= 'D' ) # create data range for time period
Date_range = pd.DataFrame(date_range) #create data frame for data range
impact_range = Date_range.merge(impact_data,how= 'left', left_on= 0, right_on = 'Date') # merge impact data to date range

# keep only the entries of the first records for rows repeating over period of days 
# (Figure out how to calculate impacts of consecutive events without summing entries more
# than once)
group = impact_range. groupby('Province')
Zambales = group.get_group('Zambales')
Zambales = Date_range.merge(Zambales, how= 'left', left_on= 0, right_on= 'Date')
Zambales.rolling('30D', on=)

for i in impact_range. groupby('Province').rolling('30D', on = 0 ):
        print(j)
    
