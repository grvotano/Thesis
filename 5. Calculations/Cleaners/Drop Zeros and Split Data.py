#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code drops Nan values in both columns are True. Initial= 2408 entries No_Nan= 1869
Splits dataframe by Province and stores in dictionary. Drop, Duplicates: 1857 - 1697
Created on Wed Apr  7 08:59:36 2021

@author: giovannivotano
"""
import csv
import pandas as pd
import matplotlib as plt
import plotly
import pickle

data = pd.read_csv(r'/Users/giovannivotano/OneDrive - UvA/Cconsecutive Disasters Thesis/DATA_BASE/7. Merge/Disasters_Cleaned.csv')

data['R_Deaths'] = data['R_Deaths'].fillna(0)
data['R_Damages'] = data['R_Damages'].fillna(0)

indexNames = data[(data['R_Deaths'] == 0) & (data['R_Damages'] == 0)].index
data.drop(indexNames , inplace=True)

data['began'] = pd.to_datetime( data['began']).dt.date
data['ended'] = pd.to_datetime( data['ended']).dt.date

#data['month_count'] = data.groupby('Province').cumcount('month')
data['duration'] = data['ended'] - data['began']

data.drop(columns= 'Unnamed: 0', inplace= True)
data = data.drop_duplicates()

rename = {GID_1_2: "Admin"}
#data.to_csv('disasters_final.csv')
# create new dataframs per Province

group = data['Province']    # groupby province
agg = data.groupby([group])

dic = {}   # empty dictionary 
for year, group in agg:    # fills dictionary with dataframes per province
   dic[group.iloc[0].Province] = pd.DataFrame(group)

# save dictionary to pickle file
pickle_out =  open( "impact_dataframes.p", "wb" )) 
pickle.dump(dic, open( "impact_dataframes.pickle", 'wb'))
open( "impact_dataframes.pickle", 'wb').close()
pickle.load(open('impact_dataframes.p', 'rb'))   
   
abra = pd.DataFrame.from_dict(dic.Keys(["Abra"]), orient = 'index', dtype = str)
   
datasum = data.groupby(['month', 'Province'],as_index=False).sum()
consecutive_disasters = count.merge(datasum, left_on= ['month', 'Province'], right_on= ['month', 'Province'])
consecutive_disasters.reset_index(level=0, inplace=True)
consecutive_disasters = consecutive_disasters[consecutive_disasters['count_col'] > 1]
consecutive_disasters.reset_index(level=0, inplace=True)   
consecutive_disasters.drop(columns= ['level_0', 'index'], inplace= True)     

# amount of consecutive disasters per Province
amount = consecutive_disasters.groupby('Province', as_index =False).count()
grp = consecutive_disasters.groupby('Province')
metro_man = grp.get_group('Metropolitan Manila')

# plot
plt.scatter(metro_man['month'], metro_man['R_Damages'], metro_man['R_Deaths'])
plt.scatter(Metropolitan_Manila['month'], Metropolitan_Manila['R_Damages'], Metropolitan_Manila['R_Deaths'])
plt.xticks(rotation= 90, fontsize= 5)
plt.yticks(fontsize= 5)
plt.title('Metro Manila Consecutive Disasters Number of Deaths', fontsize= 8, color= 'green')
plt.ylabel('Number of Deaths', fontsize= 5)
plt.tight_layout()
plt.savefig('Consecutive Disasters Per Province.png', dpi=300)
# barplot
plt.bar(amount['Province'], amount['count_col'])
plt.xticks(rotation= 90, fontsize= 5)
plt.yticks(fontsize= 5)

# Add title and axis names
plt.title('Consecutive Disasters Per Province', fontsize= 8, color= 'green')
plt.ylabel('Number of Consecutive Disasters', fontsize= 5)
plt.tight_layout()
plt.savefig('Consecutive Disasters Per Province.png', dpi=300)

group = data.groupby('Province')
Metropolitan_Manila = group.get_group('Metropolitan Manila')
Metropolitan_Manila.groupby('month').sum()

if date in data.months == data.month[i] & data.Province[i] == 

#for key, val in dic.items():
#data.drop(columns='Unnamed: 0', inplace= True)    
#count = data.groupby(['Province']).count()
count = data.groupby(['month', 'Province']).["index"].transform("count")
#count = data.groupby(['month', 'Province']).agg(count_col=pd.NamedAgg(column="Province", aggfunc="count"))
#data.groupby(['Province']).size()
# append disasters data frame with consecutive count
dis_count = pd.DataFrame(columns= )
for i in count['count_col']:
    if i > 1:
        
        

   
# create consecutive disasters dataframe
disasters = pd.DataFrame(columns=(['Province', 'Disaster Occurance', 'Consecutive Disaster Occurance']))
