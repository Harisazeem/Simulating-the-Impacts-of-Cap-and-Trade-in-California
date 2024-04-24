# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:50:41 2024

@author: haris
"""

####--------This file reads data from different sources and filters them-----##


#import modules
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona
import os
import requests


#import the Plant-level csv file
df_plants_ca = pd.read_csv("Plant-Level Data for California.csv")
df_plants_ca.info()

#Create a new column for unused capacity factor ratio for mapping in QGIS
df_plants_ca["Unused Capacity"] = 1 - df_plants_ca["Plant capacity factor"]
df_plants_ca["Annual Generation Potential (MWh)"] = df_plants_ca["Plant nameplate capacity (MW)"] * 8760 

#convert the dataframe into a geodataframe for mapping. EPSG=26945
gpd_plant_ca = gpd.GeoDataFrame(df_plants_ca, geometry=gpd.points_from_xy(df_plants_ca.longitude, df_plants_ca.latitude), crs="EPSG:4269")
gpd_plant_ca.info()

#Save gpd file as gpkg
gpd_plant_ca.to_file("gpd_plant_ca2.gpkg", layer="CAplants")


#testing the spread
plt.rcParams['figure.dpi'] = 300
fig,ax1 = plt.subplots()
gpd_plant_ca.plot(color="tan", ax=ax1)
ax1.axis("off")
fig.tight_layout()

##---------------------------------------------------------------------------##

#reading and filtering county gpd
county_gpd = gpd.read_file("tl_2023_us_county.zip")
county_gpd.info()
counties_CAL = county_gpd.query('STATEFP == "06"')

counties_CAL.to_file("counties_CAL.gpkg", layer="CountyShp")

#reading and filtering Cali tract gpd
tract_gpd = gpd.read_file("tl_2023_06_tract.zip")
tract_gpd.info()
print(len(tract_gpd["GEOID"].unique()))

##---------------------------------------------------------------------------##

#API call for calling data on Median income, Total Race, and African/American

#Add name of the original geographical entity for each row: 
#Sort of a description of the row.
#So this is the county name plus variable. We will convert this into a string.
var = ['NAME','B20002_001E', 'B02001_001E', 'B02001_002E', 'B02001_003E', 'B17001_001E']
var_string = ",".join(var)


#Setting API calls
api = 'https://api.census.gov/data/2018/acs/acs5'

#County as the level of geographical unit to be returned
for_clause = 'tract:*'

#Limiting to a larger geographical entity.
in_clause = 'state:06'

key_value = 'f3bb3c65bdc138f5936d1979e8ad880f9d26fc6f'

#Set payload for getting required variables
payload = {'get':var_string, 'for':for_clause, 'in':in_clause, 'key':key_value}

#Request the data from the endpoint
response = requests.get(api, payload)

#If statement to test if the API call worked
if response.status_code != 200:
    print(response.status_code)
    print(response.text)
    assert False
row_list = response.json()

#Set column names to the first list in row
colnames = row_list[0]

#Set data row to the remaining list
datarows = row_list[1:]

#convert this into a dataframe; and set_index at NAME
income_race = pd.DataFrame(columns=colnames, data=datarows)
income_race.set_index("NAME")

#Rename Columns
col_names = {'B20002_001E': 'median_income', 'B02001_001E': 'tot_pop', 'B02001_002E':'white_pop', 'B17001_001E':'poverty_status', 'B02001_003E':'black_african-american'}
income_race = income_race.rename(columns=col_names)
income_race.columns
income_race.info()

#Change data types of some variables to float or int
col_names = ['median_income', 'tot_pop', 'white_pop', 'poverty_status', 'black_african-american']
income_race[col_names] = income_race[col_names].astype(float)


#Add variable for POC %age
income_race['poc_pop'] = income_race['tot_pop']-income_race['white_pop']


#Create GEOID
income_race["GEOID"] = income_race['state'] + income_race['county'] + income_race['tract']
income_race.set_index("GEOID")

#Create two columns out of the demographic data 'Name' column and drop it.
#Split 'NAME' column into 'census_tract' and 'county_name'
income_race[['census_tract', 'county_name', 'state_name']] = income_race['NAME'].str.split(', ', expand=True)
income_race.drop(columns=['NAME', 'state_name'], inplace=True)

#read into csv
income_race.to_csv("income_race_demographics.csv", index='GEOID')
##---------------------------------------------------------------------------##

