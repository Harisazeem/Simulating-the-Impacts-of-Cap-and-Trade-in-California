# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 20:34:09 2024

@author: haris
"""
#import modules
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona

#----------------------------------------------------------------------------------------#


#Filtering eGrid Plant-level data
##import egrid data
columns = pd.read_excel("eGrid Plant Columns of Interest.xlsx", header=None)
columns_list = columns[0].tolist()

df_egrid = pd.read_excel("egrid2022_data.xlsx", sheet_name="PLNT22")

##read only the columns of interest
df_egrid = df_egrid[columns_list]
print(len(df_egrid.columns))

df_egrid = df_egrid.drop(0)
df_egrid.columns

##Rename columns:
cols_to_rename = {"Data Year":"Year", "Plant state abbreviation":"State", "Plant primary fuel category":"Primary fuel source", "Plant latitude": "latitude", "Plant longitude":"longitude" }
df_egrid = df_egrid.rename(columns = cols_to_rename)

##Filter plants by California
df_egrid_CA = df_egrid.query("State == 'CA'")

print(df_egrid_CA.dtypes)

##Filter data by major fuel source = Oil, Gas, Oil/Gas, and Coal
print(df_egrid_CA['Primary fuel source'].unique())
desired_sources = ['GAS', 'OIL', 'COAL']
df_egrid_CAPLNT = df_egrid_CA.query('`Primary fuel source` in @desired_sources')


#---------------------------------------------------------------------------------------------#


#Filtering eGrid Generator-level data
##import data
columns2 = pd.read_excel("eGrid Gen Columns of Interest.xlsx", header=None)
columns_list2 = columns2[0].tolist()
df_egrid_gen = pd.read_excel("egrid2022_data.xlsx", sheet_name="GEN22")

##read columns of interest
df_egrid_gen = df_egrid_gen[columns_list2]
df_egrid_gen = df_egrid_gen.drop(0)
df_egrid_gen.columns

##Rename columns
cols_to_rename2 = {"Data Year":"Year", "Plant state abbreviation":"State","Generator primary fuel":"Primary_fuel", "Number of associated boilers":"No. of Boilers"}

df_egrid_gen = df_egrid_gen.rename(columns = cols_to_rename2)

##Filter generators by California
df_egrid_CAGen = df_egrid_gen.query("State == 'CA'")

print(df_egrid_CAGen.dtypes)

##Filter data by major fuel source = Oil, Gas, Oil/Gas, and Coal
print(df_egrid_CAGen['Primary_fuel'].unique())
desired_sources2 = ["BFG", "BIT", "DFO", "KER", "LFG", "LIG", "NG", "PC", "RC", "RFO", "SUB"]
df_egrid_CAGen = df_egrid_CAGen.query('Primary_fuel in @desired_sources2')


#---------------------------------------------------------------------------------------------#


#All data types are strings. Change relevant to integer
##Change data type to float in CAPLNT
print(df_egrid_CAPLNT.columns.tolist())

vars_to_convert = ['Year', 'latitude', 'longitude', 'Number of units',
                   'Number of generators', 'Plant capacity factor', 
                   'Plant nameplate capacity (MW)', 'Nonbaseload Factor', 
                   'CHP plant useful thermal output (MMBtu)', 'CHP plant power to heat ratio', 
                   'CHP plant electric allocation factor', 'Plant annual heat input from combustion (MMBtu)', 
                   'Plant total annual heat input (MMBtu)', 'Plant annual net generation (MWh)', 
                   'Plant annual CO2 emissions (tons)', 'Plant annual CO2 equivalent emissions (tons)', 
                   'Plant annual CO2 total output emission rate (lb/MWh)', 
                   'Plant annual CO2 equivalent total output emission rate (lb/MWh)', 
                   'Plant annual CO2 input emission rate (lb/MMBtu)', 
                   'Plant annual CO2 equivalent input emission rate (lb/MMBtu)', 
                   'Plant nominal heat rate (Btu/kWh)', 'Plant annual coal net generation (MWh)', 
                   'Plant annual oil net generation (MWh)', 'Plant annual gas net generation (MWh)']


df_egrid_CAPLNT[vars_to_convert] = df_egrid_CAPLNT[vars_to_convert].astype(float)


#write to csv
df_egrid_CAPLNT.to_csv("Plant-Level Data for California.csv", index=False)







