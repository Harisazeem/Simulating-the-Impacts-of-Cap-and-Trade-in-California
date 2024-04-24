# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 13:50:11 2024

@author: haris
"""

#import modules
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona
import os
import seaborn as sns
import numpy as np
import plotly
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.colors



#import plant-level data
df_CAPLNTS = pd.read_csv("Plant-Level Data for California.csv")

#Number of Plants by Fuel Type
df_CAPLNTS.columns

# Group the DataFrame by 'Primary fuel source' and count the number of plants for each fuel type
fuel_counts = df_CAPLNTS['Primary fuel source'].value_counts()

plt.figure()
fuel_counts.plot(kind='bar', color='green') 
plt.title('Number of Plants by Primary Fuel Source') 
plt.xlabel('Primary Fuel Source') 
plt.ylabel('Number of Plants')
plt.xticks(rotation=360, ha='right')
plt.tight_layout()  
plt.show()



###------------------------------------------------------###
#Plot net generation frequency and nameplate frequency. 
#But take out the 0.99 quantiles from both
NetGen99 = df_CAPLNTS["Plant annual net generation (MWh)"].quantile(0.99)
TotCap99 = df_CAPLNTS["Plant nameplate capacity (MW)"].quantile(0.99)

trim_df_CAPLNTS = df_CAPLNTS.query(f"`Plant annual net generation (MWh)` <= {NetGen99} and `Plant nameplate capacity (MW)` <= {TotCap99}")

# Filter out NaN values from 'Plant annual net generation (MWh)' column
net_generation = trim_df_CAPLNTS['Plant annual net generation (MWh)'].dropna()

# Plot the histogram
plt.figure()
plt.hist(net_generation, color='orange', edgecolor='black')  
plt.title('Histogram of Plant Annual Net Generation')  
plt.xlabel('Plant Annual Net Generation (MWh)') 
plt.ylabel('Count')  
plt.tight_layout()  
plt.show()  

#Plot overlayed histo
for var in ["Plant annual net generation (MWh)", "Plant nameplate capacity (MW)"]:
    fig, ax1 = plt.subplots()
    sns.histplot(data = trim_df_CAPLNTS, x = var, hue = 'Primary fuel source', kde = True, ax = ax1)
    fig.tight_layout()
    fig.savefig(f"res_{var}.png")
###-----------------------------------------------------###

#Distribution of Co2e emissions in tons
plt.figure()
plt.hist(df_CAPLNTS["Plant annual CO2 equivalent emissions (tons)"], color='green', edgecolor='black')  
plt.title('Plant-level CO2e Emissions')  
plt.xlabel('Emissions') 
plt.ylabel('Plants')  
plt.tight_layout()  
plt.show()  

