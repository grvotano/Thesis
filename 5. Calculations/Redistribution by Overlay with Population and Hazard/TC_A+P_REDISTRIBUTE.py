#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 11:56:28 2021
This code uses the aggregated earthquake hits per municipality and scores them from 1-5
The resulting scores are used to redistribute impact data based on the ratio
of aggregated scores per province hit over the total scores per disaster.
'R = I * Ptotalscore/Dtotalscore'
@author: giovannivotano
"""

import math
import pandas as pd
import numpy as np

# data
#municipalities = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/4.Hazard Data/TC/Redistribution/Municipal_Areas.csv')
municipalities = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/GADM + Geometry .csv')
tc = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/4.Hazard Data/TC/TC_buffer.csv')
disaster = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/5.Calculations/Flood/CSV/flood+tc_impact.csv')
population = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/6. Population Manipulation/Population Density by Municipality.csv')

# clean
rename = {'Unnamed: 0': 'Municipalities'}
tc = tc.rename(columns=rename)
disaster['date'] = pd.to_datetime(disaster[('began')]).dt.strftime('%Y-%m-%d')
disaster = disaster.sort_values(by="date").reset_index()
disaster_dates = disaster['date'].unique()
tc = tc.merge(municipalities, left_on= 'Municipalities', right_on='GID_2')
tc = tc.merge(population, left_on= 'Municipalities', right_on='GID_2')

list_provinces = []


#print(tc.columns.intersection(disaster_dates_complete)) # selects 80 columns
impact_match_hazard_dates = tc.columns.intersection(disaster_dates).tolist()
impact_match_hazard_dates.append('area', '_sum', 'Municipalities')
tc = tc[tc.columns.intersection(impact_match_hazard_dates)]
impact_match_hazard_dates = tc.columns.intersection(disaster_dates).tolist()
#flood_tc_impacts_dates_macthed = tc_flood[:, ()]
#all_dates =tc.columns.tolist()

# go through list of disasters, create list of affected provinces for each diaster (primary key is date)
#for date in disaster_dates:
for date in impact_match_hazard_dates:
    
    provinces = []

    for i in range(len(disaster)):
        if disaster.iloc[i].date == date:
            provinces.append([disaster.iloc[i].GID_1_2, 0, 0])
            
    list_provinces.append([date, provinces,0, 0])

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
    population_total = 0
    province_count = 0
    for province in province_list:
        # set num municipalities affected for this province to 0

        area_per_province = 0
        pop_per_province = 0
        
        #count number of munipalities
        for i in range(len(municipalities)):
            if municipalities.iloc[i].GID_1 == province[0]:
                
                mun_code = municipalities.iloc[i].GID_2

                # go through list of impacts and check if municipality is affected on date

                for j in range(len(tc)):
                    if tc.iloc[j].loc[date_of_disaster]:
                        if (isinstance(tc.iloc[j].loc[date_of_disaster], str)) and (tc.iloc[j].Municipalities == mun_code):

                            area_per_province += tc.iloc[j].area
                            pop_per_province += tc.iloc[j]._sum
                            population_total += tc.iloc[j]._sum
                            area_total += tc.iloc[j].area

        list_provinces[disaster_count][1][province_count][1] = area_per_province
        list_provinces[disaster_count][1][province_count][2] = pop_per_province
        province_count += 1
        
    list_provinces[disaster_count][2] = area_total
    list_provinces[disaster_count][3] = population_total
    disaster_count += 1

print("List provinces post processing")                        
print(list_provinces)              
            
        # store this with corresponding province
        

#make your new fkn columns

disaster['R_Deaths'] = "0"
disaster['R_Damages'] = "0"
disaster.iloc[0].R_Deaths = "7"
disaster = disaster.reset_index()

for dis in list_provinces:
    dis_date = dis[0]
    provinces = dis[1]
    total_municipalities = dis[2]
    total_pop = dis[3]
    for province in provinces:
        for i in range(len(disaster)):
            if dis_date == disaster.iloc[i].date:
                if province[0] == disaster.iloc[i].GID_1_2:
                    prov_num_mun = province[1]
                    prov_num_pop = province[2]
                    normalized = disaster.iloc[i].loc['normalised']
                    damage = disaster.iloc[i].loc['n_damage_U']
                    if total_municipalities > 0:    
                        new_normal = normalized * (((prov_num_mun / total_municipalities) + (prov_num_pop / total_pop))/2)
                        new_damage = damage * (((prov_num_mun / total_municipalities) + (prov_num_pop / total_pop))/2)
                        #damage * prov_num_mun / total_municipalities * prov_num_pop / total_pop
                    else:
                        new_normal = 0
                        new_damage = 0
                    #print(new_normal)
                    disaster.at[i, 'R_Deaths'] = new_normal
                    disaster.at[i, "R_Damages"] = new_damage
                    print(disaster.iloc[i].R_Deaths)
                    #
# export dataframe with the newly populated R_Deaths and R_Damages columns 
#tc_flood.to_csv(r'TC_R_Impacts(80 of the disasters.csv)')
#impact_match_hazard_dates.to_csv(r'dates_of_matched_tc_to_remove_unmatched_entries.csv')

#df_matched_impact_disaster = pd.DataFrame(columns=disaster.columns)
#df_unmatched_entries = pd.DataFrame(columns=disaster.columns)
#for date_i in impact_match_hazard_dates:
#    for i in range(len(disaster['date'])):
#        if disaster.iloc[i].date == date_i:
#            df_matched_impact_disaster.loc[i] = disaster.iloc[i]
#        else:
#            df_unmatched_entries.loc[i] = disaster.iloc[i]
data_matched_impact_disaster = disaster[disaster['date'].isin(impact_match_hazard_dates)]
#df_unmatched_entries = disaster[~disaster['date'].isin(impact_match_hazard_dates)]

# export redistrubuted data
data_matched_impact_disaster = data_matched_impact_disaster.reset_index()
data_matched_impact_disaster.drop(columns= "index", inplace= True)
data_matched_impact_disaster.to_csv(r'TC_R_A+P_impacts.csv') 
# unmatched entries
#df_unmatched_entries.drop(columns= "level_0", inplace= True)
#df_unmatched_entries = df_unmatched_entries.reset_index()
#df_unmatched_entries.to_csv(r'EQ_NR_impacts.csv') 