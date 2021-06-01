#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code redistributes impacts according to count of municipal admin areas within a province 
and creates a ratio per province of recorded municipal areas hit by a particular distaster 
over the aggregate total municipal areas within the total amount of provinces hit by a prticular
disaster. This ratio is applied to damages and deaths per entry per province
Created on Tue Mar  2 10:44:10 2021

@author: giovannivotano
"""

import math
import pandas as pd
import numpy as np


# data
municipalities = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/GADM + Geometry .csv')
tc = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/4.Hazard Data/TC/TC_buffer.csv')
disaster = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Flood/CSV/flood+tc_impact.csv')


# clean
rename = {'Unnamed: 0': 'Municipalities'}
tc = tc.rename(columns=rename)
disaster['date'] = pd.to_datetime(disaster[('began')]).dt.strftime('%Y-%m-%d')
disaster = disaster.sort_values(by="date")
disaster_dates = disaster['date'].unique()
tc = tc.merge(municipalities, left_on= 'Municipalities', right_on='GID_2')


list_provinces = []

#print(tc.columns.intersection(disaster_dates_complete)) # selects 80 columns
impact_match_hazard_dates = tc.columns.intersection(disaster_dates).tolist()
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
    area_total = 0
    province_count = 0
    for province in province_list:
        # set num municipalities affected for this province to 0
        area_per_province = 0
            
        #count number of munipalities
        for i in range(len(municipalities)):
            if municipalities.iloc[i].GID_1 == province[0]:
                
                mun_code = municipalities.iloc[i].GID_2

                # go through list of impacts and check if municipality is affected on date

                for j in range(len(tc)):
                    if tc.iloc[j].loc[date_of_disaster]:
                        if (isinstance(tc.iloc[j].loc[date_of_disaster], str)) and (tc.iloc[j].Municipalities == mun_code):
                            #b_date = True
                            area_per_province += tc.iloc[j].area
                            area_total += tc.iloc[j].area
                      
                    
        #print("num municiplaties per province:")
        #print(m_per_province)
        #province[1] = m_per_province
        list_provinces[disaster_count][1][province_count][1] = area_per_province
        province_count += 1
        
    #print("Total municipalities per disaster")
    #print(m_total)
    #disaster[2] = m_total
    list_provinces[disaster_count][2] = area_total
    disaster_count += 1

print("List provinces post processing")                        
print(list_provinces)              
            
        # store this with corresponding province
        


#print(tc.columns)
#print(disaster_dates)

#make your new columns

disaster['R_Deaths'] = "0"
disaster['R_Damages'] = "0"
disaster.iloc[0].R_Deaths = "7"
disaster = disaster.reset_index()

for dis in list_provinces:
    dis_date = dis[0]
    provinces = dis[1]
    total_municipalities = dis[2]
    for province in provinces:
        for i in range(len(disaster)):
            if dis_date == disaster.iloc[i].date:
                if province[0] == disaster.iloc[i].GID_1_2:
                    prov_num_mun = province[1]
                    normalized = disaster.iloc[i].loc['normalised']
                    damage = disaster.iloc[i].loc['n_damage_U']
                    if total_municipalities > 0:    
                        new_normal = normalized * prov_num_mun / total_municipalities
                        new_damage = damage * prov_num_mun / total_municipalities
                    else:
                        new_normal = 0
                        new_damage = 0
                    #print(new_normal)
                    disaster.at[i, 'R_Deaths'] = new_normal
                    disaster.at[i, "R_Damages"] = new_damage
                    print(disaster.iloc[i].R_Deaths)
                    

df_matched_impact_disaster = disaster[disaster['date'].isin(impact_match_hazard_dates)]
df_unmatched_entries = disaster[~disaster['date'].isin(impact_match_hazard_dates)]        

# export data 
df_matched_impact_disaster.drop(columns= "index", inplace= True)
df_matched_impact_disaster = df_matched_impact_disaster.reset_index()
df_matched_impact_disaster.to_csv(r'Tropical Cyclone Redistribute By Direct Hazard.csv') 

df_unmatched_entries.drop(columns= "level_0", inplace= True)
df_unmatched_entries = df_unmatched_entries.reset_index()
df_unmatched_entries.to_csv(r'Tropical Cyclone Not Redistribute By Direct Hazard.csv')              
                    