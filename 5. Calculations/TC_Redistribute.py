#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code redistributes impacts according to count of municipal admin areas within a province 
and creates a ratio per province of recorded municipal areas hit by a particular distaster 
over the aggregate total municipal areas within the total amount of provinces hit by a prticular
disaster. This ratio is applied to damages and deaths per entry per province

Created on Wed Feb 24 17:41:22 2021

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
tc = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/4.Hazard Data/TC/TC_buffer.csv')
disaster = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/4.Hazard Data/TC/Redistribution/TC_Impacts.csv')


# clean
rename = {'Unnamed: 0': 'Municipalities'}
tc = tc.rename(columns=rename)
disaster['date'] = pd.to_datetime(disaster[('began')]).dt.strftime('%Y-%m-%d')
disaster = disaster.sort_values(by="date")
disaster_dates = disaster['date'].unique()


list_provinces = []

# filter to select matching entries on date
tc_flood = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Flood/CSV/flood+tc_impact.csv')    
tc_flood['date'] = pd.to_datetime(tc_flood[('began')]).dt.strftime('%Y-%m-%d')
tc_flood = tc_flood.sort_values(by="date")
disaster_dates_complete = tc_flood['date'].unique()

#print(tc.columns.intersection(disaster_dates_complete)) # selects 80 columns
impact_match_hazard_dates = tc.columns.intersection(disaster_dates_complete).tolist()
#flood_tc_impacts_dates_macthed = tc_flood[:, ()]
#all_dates =tc.columns.tolist()

#print(disaster_dates)
#print(impact_match_hazard_dates)

# go through list of disasters, create list of affected provinces for each diaster (primary key is date)
#for date in disaster_dates:
for date in impact_match_hazard_dates:
    
    provinces = []

    for i in range(len(disaster)):
        if disaster.iloc[i].date == date:
            provinces.append([disaster.iloc[i].GID_1_2, 0])
            
    list_provinces.append([date, provinces,0])

print("List of provinces pre processing")
print(list_provinces)
# go through each disaster, get the date and and list of provinces for each

disaster_count = 0

for dis in list_provinces:
    
    #get date and provinces affected
    date_of_disaster = dis[0]
    province_list = dis[1]

    #go through list of provinces. Foreach province, check what munipalities have been affected
    m_total = 0
    province_count = 0
    for province in province_list:
        # set num municipalities affected for this province to 0
        m_per_province = 0
            
        #count number of munipalities
        for i in range(len(municipalities)):
            if municipalities.iloc[i].GID_1 == province[0]:
                
                mun_code = municipalities.iloc[i].GID_2

                # go through list of impacts and check if municipality is affected on date

                for j in range(len(tc)):
                    if tc.iloc[j].loc[date_of_disaster]:
                        if (isinstance(tc.iloc[j].loc[date_of_disaster], str)) and (tc.iloc[j].Municipalities == mun_code):
                            #b_date = True
                            m_per_province += 1
                            m_total += 1
                      
                    
        #print("num municiplaties per province:")
        #print(m_per_province)
        #province[1] = m_per_province
        list_provinces[disaster_count][1][province_count][1] = m_per_province
        province_count += 1
        
    #print("Total municipalities per disaster")
    #print(m_total)
    #disaster[2] = m_total
    list_provinces[disaster_count][2] = m_total
    disaster_count += 1

print("List provinces post processing")                        
print(list_provinces)              
            
        # store this with corresponding province
        


#print(tc.columns)
#print(disaster_dates)

#make your new fkn columns

tc_flood['R_Deaths'] = "0"
tc_flood['R_Damages'] = "0"
tc_flood.iloc[0].R_Deaths = "7"
tc_flood = tc_flood.reset_index()

for dis in list_provinces:
    dis_date = dis[0]
    provinces = dis[1]
    total_municipalities = dis[2]
    for province in provinces:
        for i in range(len(tc_flood)):
            if dis_date == tc_flood.iloc[i].date:
                if province[0] == tc_flood.iloc[i].GID_1_2:
                    prov_num_mun = province[1]
                    normalized = tc_flood.iloc[i].loc['normalised']
                    damage = tc_flood.iloc[i].loc['n_damage_U']
                    if total_municipalities > 0:    
                        new_normal = normalized * prov_num_mun / total_municipalities
                        new_damage = damage * prov_num_mun / total_municipalities
                    else:
                        new_normal = 0
                        new_damage = 0
                    #print(new_normal)
                    tc_flood.at[i, 'R_Deaths'] = new_normal
                    tc_flood.at[i, "R_Damages"] = new_damage
                    print(tc_flood.iloc[i].R_Deaths)
                    #
                    
    
# export dataframe with the newly populated R_Deaths and R_Damages columns 
#tc_flood.to_csv(r'TC_R_Impacts(80 of the disasters.csv)')
impact_match_hazard_dates.to_csv(r'dates_of_matched_tc_to_remove_unmatched_entries.csv')
df_unmatched_entries = pd.DataFrame(columns=tc_flood.columns)
for date_i in impact_match_hazard_dates:
    for i in range(len(tc_flood['date'])):
        if tc_flood.iloc[i].date != date_i:
            df_unmatched_entries.loc[i] = tc_flood.iloc[i]



