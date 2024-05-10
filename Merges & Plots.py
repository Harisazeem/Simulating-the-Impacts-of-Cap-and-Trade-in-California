# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:32:58 2024

@author: haris
"""

#Import modules
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona
import os
import numpy as np
import seaborn as sns

#Import files to be merged and experimented with
tracts = gpd.read_file("tl_2023_06_tract.zip", dtype={'GEOID':str})
plants_ca = gpd.read_file("gpd_plant_ca2.gpkg", layer="CAplants")
income_race_demos = pd.read_csv("income_race_demographics.csv", dtype = {'GEOID': str})

#Clean up tract columns a bit. Discard the ones not needed.
columns_to_keep = ["GEOID", "GEOIDFQ", "NAME", "geometry"]
tracts = tracts[columns_to_keep]
tracts.set_index("GEOID")


#Merges and Joins

#1. Join tracts with plants df. This will give plants by tract. It will leave tracts without plants
#but we will deal with that later.
plants_tracts = plants_ca.sjoin(tracts, how="left", predicate="within") #left is within right
print(plants_tracts["geometry"].value_counts(dropna=False))
plants_tracts.set_index("GEOID") #We got a layer with plants within tracts. 
#We're left with left geometries only though. But now we have data for the tracts as well. 


#2. Group plant_tract by GEOID
list_column = plants_tracts.columns

col_names_agg = {"Plant name":"size", "Plant county name":"unique", "Plant nameplate capacity (MW)":"sum",
                 "Plant annual net generation (MWh)":"sum", "Plant annual CO2 emissions (tons)":"sum",
                 "Plant annual CO2 equivalent emissions (tons)":"sum", 
                 "Plant annual CO2 equivalent total output emission rate (lb/MWh)":"max", 
                 "Unused Capacity":"sum", "Annual Generation Potential (MWh)":"sum"}

grouped_plant_tract = plants_tracts.groupby("GEOID").agg(col_names_agg)

list_columns = grouped_plant_tract.columns.to_list()


##-------------------------Visualizations-----------------------------##

#Top 10 Census Tracts with highest number of power plants
top_10_geoids = grouped_plant_tract['Plant name'].nlargest(10)

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', 
          '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

plt.figure(figsize=(10, 6))
top_10_geoids.plot(kind='bar', color=colors)
plt.title('Top 10 GEOIDs with Highest Plant Counts')
plt.xlabel('GEOID')
plt.ylabel('Number of Plants')
plt.xticks(rotation=45)
plt.show()

#Top 10 Census Tracts with highest emission levels
top_10_geoids_emissions = (grouped_plant_tract['Plant annual CO2 equivalent emissions (tons)']/1000000).nlargest(10)

plt.figure(figsize=(10, 6))
top_10_geoids_emissions.plot(kind='bar')
plt.title('Top 10 GEOIDs with Highest Emission Levels')
plt.xlabel('GEOID')
plt.ylabel('Emissions per Tract (Million Tons)')
plt.xticks(rotation=45)
plt.show()

#Top 10 Census Tracts with highest Annual Generation Potential
# Assuming grouped_plant_tract is your DataFrame
top_10_gen_cap = grouped_plant_tract["Annual Generation Potential (MWh)"].nlargest(10)

# Define custom darker colors
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# Plotting
plt.figure(figsize=(10, 6))
top_10_gen_cap.plot(kind='bar', color=colors)
plt.title('Top 10 Census Tracts with Highest Annual Generation Potential')
plt.xlabel('Census Tract')
plt.ylabel('Generation Potential')
plt.xticks(rotation=45)
plt.show()


#####--------------------------------------------------------------------------------####

# 3. Further Merging of grouped_plant_tract with demographic data per census tract
tract_plant_demo = grouped_plant_tract.merge(income_race_demos, on="GEOID", validate='1:1', indicator=True)
print(tract_plant_demo['_merge'].value_counts()) #it is a perfect one-to-one match
tract_plant_demo.drop(columns='_merge', inplace=True)
tract_plant_demo.set_index("GEOID")
#Now this dataframe has all census tracts which have power plants in them. And it contains
#demographic information for them.


# 4. Merge this data, which contains information on tracts with plants and their demos, with the tracts gpd data.
## that will give us all tracts, including the ones with no plants if this was not an inner join, 
## and their geometries for plotting. 
Tract_Plant_Demo_All = tracts.merge(tract_plant_demo, on="GEOID")

#Separately merge All tracts with their demographic information. 
income_race_demos.set_index("GEOID")
Tract_Demo_AllTracts = tracts.merge(income_race_demos, on="GEOID", how="outer")

Tract_Demo_AllTracts.info()

#Last merge for now: Merge Plant_Tract(ungrouped) with tract-level demos. 
Plant_Tracts_Demo = plants_tracts.merge(income_race_demos, on="GEOID", how="left")



#Create Layers and GeoPackageFiles
##For Tract_PLNT_Demo_All file. Contains information on only those tracts with plants on them. 
Tract_Plant_Demo_All = Tract_Plant_Demo_All.drop(columns=["GEOIDFQ", "Plant county name", "Unused Capacity", "state",])
Tract_Plant_Demo_All.to_file("Tract_Plant_Demo_All.gpkg", layer="TractPLNTDemo")

##For Tract_Demo_AllTract. Information on all tracts and their demographic information
Tract_Demo_AllTracts.to_file("Tract_Demo_AllTracts.gpkg", layer="TractDemo")

##For Plants_Tract_Demo Data
Plant_Tracts_Demo.to_csv("Plant_Tracts_Demo.csv")






#####----------Other Visualizations Based on Data Created Here-----------#####

#Correlation matrix on Track_Plant_Demo_All data
columns_of_interest = ['Plant name', 'Plant annual net generation (MWh)', 
                       'Plant annual CO2 emissions (tons)', 'Annual Generation Potential (MWh)', 
                       'median_income', 'poverty_status', 'poc_pop']

# Rename the 'Plant name' column to 'No. of Plants'
Tract_Plant_Demo_Selected = Tract_Plant_Demo_All[columns_of_interest].rename(columns={'Plant name': 'No. of Plants',
                                                                                      'Plant annual net generation (MWh)':'Tract net generation (MWh)',
                                                                                      'Plant annual CO2 emissions (tons)':'Tract CO2 emissions',
                                                                                      'Annual Generation Potential (MWh)':'Tract Gen Potential (MWh)'
                                                                                      })

# Compute the correlation matrix
correlation_matrix = Tract_Plant_Demo_Selected.corr()

# Set up the matplotlib figure
plt.figure(figsize=(10, 8))

# Create a heatmap of the correlation matrix using seaborn
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")

# Add a title
plt.title('Correlation Matrix')

# Show the plot
plt.show()
plt.savefig("Correlation Matrix - Tracts and Plants")








