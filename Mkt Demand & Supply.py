# -*- coding: utf-8 -*-
"""
Created on Fri May  3 05:40:05 2024

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
import scipy.optimize as opt
from scipy.optimize import brentq
import copy



#import plant_tracts_demo
Plant_Tracts_Demo = pd.read_csv("Plant_Tracts_Demo.csv")

#separate all the CO2e emissions. We are assuming these are the ones which the Power Plants have the
##permit for 
Plant_Tracts_Demo.columns

columns_needed = ["Plant name", "Plant annual CO2 equivalent emissions (tons)"]
co2e_permits = Plant_Tracts_Demo[columns_needed]
co2e_permits.info()

#exclude N/A. we would be left with 228 plants
co2e_permits = co2e_permits.dropna()



#####Calibration Purposes####

#Constant Elasticity Demand Curve. Call it elast

#Step 1: Individual function to determine Ai: qi=Ai*P**-ei where ei is the elasticity.
#Define a function that calculates Ai for
def calculate_Ai(df, price:float, elast:float):
    Ai = df['Plant annual CO2 equivalent emissions (tons)']/(price ** elast)
    return Ai

#Step 3: Create another function which measures Q based on Ai, Pr, and Elast. Create a new dataframe. 
def calculate_ind_q(Ai, price:float, elast:float):
    ind_q_prmts = Ai * price ** elast
    Ai = pd.DataFrame(Ai)
    Ai = Ai.rename(columns={'Plant annual CO2 equivalent emissions (tons)':'Ai'})
    Ai['Permits'] = ind_q_prmts
    return Ai


#Step 4: Test that with price, elasticity, and dataframe. Average auction price $32.93. This would
#be our base Ai with -1.0 elasticity for every pp. 
df = co2e_permits
price = 32.93
elast = -1.0

Ai_base = calculate_Ai(co2e_permits, price, elast)

Ind_permits = calculate_ind_q(Ai_base, price, elast)

#Ai_Alt 
#Uptill here all numbers match and everyhting checks out



#Step 5: Measure the mkt_demand
def mkt_demand(Ai, price:float, elast:float):
    Indiv_permits = calculate_ind_q(Ai, price, elast)
    mkt_demand = Indiv_permits['Permits'].sum()
    return mkt_demand


qd_base_mkt = mkt_demand(Ai_base, price, elast)



###Test mkt demand###



#Do a reverse from sum to individual. Use the excess demand route. 


#Step 6: Calculate market supply. I am treating it as emissions allowed * total market demand. 
#For market demand here, either we give a number (or a column) separately or we use the aforementioned fucntion
emission_allowance = qd_base_mkt
    

#Step 7: Calculate excess_demand:
def excess_mkt_d(price:float, Ai, elast:float, emission_allowance:float):
    market_demand = mkt_demand(Ai, price, elast)
    excess_mkt_d = market_demand - emission_allowance
    return excess_mkt_d

#testing
excess_mkt_d(price*1.1, Ai_base, elast, emission_allowance)
#%% 

#Caliberation and testing the impact of price on individual permit demand based on same elasticity for all power plants. 

#Step 8: Use excess demand to find a price. This needs to be the same as the price we used earlier.
guess = 20
mkt_price = opt.newton(excess_mkt_d, guess, maxiter=100, args=[Ai_base, elast, emission_allowance])
print("The price demanded for the equilibrium of market supply & demand: ", mkt_price)

#Individual Qs at baseline
Ind_Permits_Base_Cal = calculate_ind_q(Ai_base, mkt_price, elast)

#Emission Allowance at 10% reduction: policy 1
mkt_price = opt.newton(excess_mkt_d, guess, maxiter=100, args=[Ai_base, elast, emission_allowance*0.9])
print("The price demanded for the equilibrium of market supply & demand: ", mkt_price)

#Individual Qs in Policy 1
Ind_Permits_Policy1 = calculate_ind_q(Ai_base, mkt_price, elast)


#Ind permits policy/ ind permits baseline
prct = 100*(Ind_Permits_Policy1/Ind_Permits_Base_Cal-1) #For percentage

#The prct dataframe shows that every power plant would reduce emissions by 10% in response to
#a decrease in emission_allowance by 10%.This is what would happend in a command_and_control policy
#where every power plant is asked to reduce emissions by a certain percentage. 
    




#%%

#Now let's test a simulation where some power plants have different elasticities. First case has 
#0.75 elasticity for top three polluters. Remember a change in elasticities would affect Ai as well. 

#create different elasts. 1.50 for biggest three polluters since they emit the most. The idea is
#that elasticity is higher for those power plants which are more expensive to clean. 
co2e_permits_diff_elasts = co2e_permits
co2e_permits_diff_elasts['elast'] = -1.0
top_three_indices = co2e_permits_diff_elasts['Plant annual CO2 equivalent emissions (tons)'].nlargest(3).index
co2e_permits_diff_elasts.loc[top_three_indices, 'elast'] = -1.50
co2e_permits_diff_elasts = co2e_permits_diff_elasts.sort_values(by='elast')
diff_elasts = co2e_permits_diff_elasts['elast'] #To have it as a separate series
co2e_permits.drop(columns='elast', inplace=True)


#Now finds their Ai; it would be alternate Ai
df = co2e_permits
price = 32.93
elast = diff_elasts
Ai_alt = calculate_Ai(co2e_permits, price, elast)


#base emission_allowance would be same as well
emission_allowance = qd_base_mkt

#Price different with different elasts and policy 1.1 (different elasts) scenario where emissions reduce by 10%
guess = 20
mkt_price = opt.newton(excess_mkt_d, guess, maxiter=100, args=[Ai_alt, elast, emission_allowance*0.9])
print("The price demanded for the equilibrium of market supply & demand: ", mkt_price)

#Individual Qs in Policy 1.1
Ind_Permits_Policy1_1 = calculate_ind_q(Ai_alt, mkt_price, elast)

#Ind permits policy/ ind permits baseline
prct1_1 = 100*(Ind_Permits_Policy1_1/Ind_Permits_Base_Cal-1) #For percentage

#This shows that biggest polluters, with larger elasts and lower MACs,
#reduce more compared to command-and-control policy. 


#%%

#A function which goes through elasts, base price, base quantities, to calculate Ai.
#Then sums up the base quantitites to come up with base market demand.
#Then uses emission_allowance as another argument to have market supply.
#Then runs opt.newton to find new mkt_price2
#Then uses that to find Individual quantities using Ai, new mkt price, and elast


#The following Plant data should have at least two columns: their total CO2e emissions and elasticities.

def magnum_opus(PLNT_data, base_price:float, reduction_trgt, guess=20): #reduction target should be a ratio e.g., 0.1 if 10% reduction or 0 if no reudction
    Ai = calculate_Ai(PLNT_data, base_price, PLNT_data['elast'])
    base_mkt_dmnd = PLNT_data['Plant annual CO2 equivalent emissions (tons)'].sum()
    emission_allowance = base_mkt_dmnd * (1-reduction_trgt) #emission_allowance acts as mrkt_supply
    mkt_price2 =  opt.newton(excess_mkt_d, guess, maxiter=100, args=[Ai, PLNT_data['elast'],emission_allowance])
    ind_prmts_p2 = calculate_ind_q(Ai, mkt_price2, PLNT_data['elast'])
    prct_chng = 100*(ind_prmts_p2['Permits']/PLNT_data['Plant annual CO2 equivalent emissions (tons)']-1)
    PLNT_data['prmts_post_reduction'] = ind_prmts_p2['Permits']
    PLNT_data[f'prct_change_permits with {reduction_trgt*100}% reduction'] = prct_chng
    return PLNT_data


#Test this:
co2e_permits_test = co2e_permits
co2e_permits_test['elast'] = -1.0
top_three_indices = co2e_permits_test['Plant annual CO2 equivalent emissions (tons)'].nlargest(3).index
co2e_permits_test.loc[top_three_indices, 'elast'] = -1.50
co2e_permits_test = co2e_permits_test.sort_values(by='elast')
co2e_permits.drop(columns='elast', inplace=True)

c02e_permits_test2 = magnum_opus(co2e_permits_test, base_price=32.93, reduction_trgt=0.1)


#%%
###Now we will find percentage change in emissions based on three scenarios:
###a. baseline cmmnd&cntrl policy when all have same elasticities, b. big polluters with high elast, c.big polluters with low elast

#a. baseline cmmnd&cntrl has already been done by us. Let's put that into a separate dataframe for later use
co2e_permits_cmmnd_ctrl = copy.deepcopy(co2e_permits)
co2e_permits_cmmnd_ctrl['elast']=-1.0

#with 20% reduction in emissions
magnum_opus(co2e_permits_cmmnd_ctrl, base_price=32.93, reduction_trgt=0.2)

#b. Big polluters with high elast(lower MACs). Big polluters with emissions greater than 250k tons per year
co2e_permits_high_elast = copy.deepcopy(co2e_permits)
co2e_permits_high_elast['elast'] = -1 
co2e_permits_high_elast.loc[co2e_permits_high_elast['Plant annual CO2 equivalent emissions (tons)'] > 250000, 'elast'] = -2.1

magnum_opus(co2e_permits_high_elast, base_price=32.93, reduction_trgt=0.2) #20% reduction in emissions

#c. Big polluters with lower elast (high MACs). Big polluters with emissions greater than 250k tons
co2e_permits_low_elast = copy.deepcopy(co2e_permits)
co2e_permits_low_elast['elast'] = -1 
co2e_permits_low_elast.loc[co2e_permits_high_elast['Plant annual CO2 equivalent emissions (tons)'] > 250000, 'elast'] = -0.5

magnum_opus(co2e_permits_low_elast, base_price=32.93, reduction_trgt=0.2)

#%%

###Merging and Mapping the Three Scenarios