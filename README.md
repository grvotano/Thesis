# Thesis
Repository of all codes to process data for my Earth Science Master Thesis. My thesis topic is "Constructing a Framework to Analyse the Impacts of Consecutive Disasters: Case Study, The Philippines". Three main types of data are used in this project. These are Impact, Hazard and Exposure Data. the main objective of this thesis is to improve the Sptatial and Temporal resolution of Impact data.
 
# Codes to process the impact, exposure  and hazard data are arranged according to the following Steps
- 1. Clean
- 2. Merge
- 3. Spatial Reference
- 4. Normalise 
- 5. Hazard Data Preprocessing 
- 6. Calculations

# Notable issues that need improvement 

a. An important task is to improve the spatial resolution of the impact data that is gathered. To do this, impact data entries need to first be spatially referenced and then overlay with hazard data to accurately identify to what extent areas at a higher spatial resolution (provincial in this case) are hit. In many of the disasters the corresponding administrative areas are not found in the hazard data for a particular date. This could be a result of 1. Inaccurate recording of areas hit in the impact data 2. inaccurate recording of dates in impact or hazard data 3. not all disasters wehre recorded in either imapact or hazard data frames
Reccomended solutions :  1. improve quality of data sets by going through each disaster and making sure (via research online) dates and areas are correctly recorded or 2. updating the hazard impact overlay code by upgrading the filtering by date to add a buffer on the date selection.


