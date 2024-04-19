# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:50:41 2024

@author: haris
"""

####--------This file reads the data from the plant file for visualizations--------####



#import modules
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona
import os


#import the Plant-level csv file
df_plants_ca = pd.read_csv("Plant-Level Data for California.csv")
df_plants_ca.info()

#Create a new column for unused capacity factor ratio for mapping in QGIS
df_plants_ca["Unused Capacity"] = 1 - df_plants_ca["Plant capacity factor"]


#convert the dataframe into a geodataframe for mapping. EPSG=26945
gpd_plant_ca = gpd.GeoDataFrame(df_plants_ca, geometry=gpd.points_from_xy(df_plants_ca.longitude, df_plants_ca.latitude), crs="EPSG:4269")
gpd_plant_ca.info()

#Save gpd file as gpkg
gpd_plant_ca.to_file("gpd_plant_ca.gpkg", layer="CAplants")


#testing the spread
plt.rcParams['figure.dpi'] = 300
fig,ax1 = plt.subplots()
gpd_plant_ca.plot(color="tan", ax=ax1)
ax1.axis("off")
fig.tight_layout()

#reading and filtering county gpd
county_gpd = gpd.read_file("tl_2023_us_county.zip")
county_gpd.info()
counties_CAL = county_gpd.query('STATEFP == "06"')

counties_CAL.to_file("counties_CAL.gpkg", layer="CountyShp")

