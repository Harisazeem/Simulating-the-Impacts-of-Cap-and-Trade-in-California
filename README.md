# Abstract

This project provides an analysis of California's fossil-fueled power plants and their response to different emission reduction policy scenarios. An exploratory analysis is followed by emission-reduction simulations under market-driven cap-&-trade and command-&-control policies to comprehend the emission reduction behavior of different types of power plants.

# Methodology and Data

The data used for this analysis has been sourced from multiple sources. Plant-level data is sourced from EPA's Emissions & Generation Resource Integrated Database. Census tract information and ACS demographic data for California's census tracts have been sourced from census burea web interface. 

Firstly, plant level data—which includes plant specific information, such as geolocation, annual emissions (tons), and heat rates—is filtered to California's census tract level. Only fossil-fueld power plants, running on Gas, Oil, and Oil, are included for emission reduction scenarios. Secondly, this plant-level data is merged with census tracts and demographic information for exploratory data analysis. Thirdly, market demand and supply functions for emission reduction are created to simulate how different power plants would respond to different policy scenarios under permit trading and command & control policies. Fourthly, the response of power plants is mapped on California's census tract level to see how different power plants—differentiated through their annual emissions, percentage reduction in emission levels, and tract-based location—would respond to the given scenario. These final maps exist in form of interactive html files.  

QGIS, geopandas, and folium module in Python are used for mapping purposes throughout this analysis. 

# Scripts

1. Filtering egrid.py filters national level data on plants and generators by fossil-fueled power plants in California. 

2. Mapping plant-level data.py adds information on unused capacity and total possible annual generation for each power plant in California. It then reads and filters census files. It tests the spread of the power plant point location and imports demographic information for California's census tracts using an API call. 

3. Merges Plots.py filters, spatially joins, and groups data on power plants by census tracts and their demographic information. It then visualized some of the information for exploratory data analysis. Data visualized here includes top 10 census tracts with highest number of power plants, highest emission levels, highest annual generation potential, and a correlation matrix for power plant and demographic information. The script finally creates several geopackage files containing the merged data.

4. Other Visualization.py creates more visualizations for exploratory data analysis. These include overlayed histograms for net generation frequency, nameplate frequence, and distribtion of Co2 equivalent emissions in tons. 

5. Mkt Demand Supply.py creates and calibrates individual and market demand functions for carbon trading by each power plant. This caliberation is based on baseline information on total annual carbon emissions in 2022 and the carbon price in California's permit trading system. The market demand and market supply functions are then used to calculate new market price based on different emission targets using the opt.newton optimization method. A final function (called magnum_opus) is created, which takes intital plant-level emission, price, and emission-reduction target, to find new market price and individual demand for permits under different policy scenarios. The function is used to measure emission reduction by each individual plant using three hypothetical scenarios: A Command and Control policy for 20% state-level emission reduction where all power plants have the same elasticity of demand for permits, a permit-trading scenario for 20% state-level reduction where bigger polluters (those emitting more than 250,000 tons of Co2) have higher elasticities than rest, and a permit-trading scenario for 20% reduction where bigger polluters (those emitting more than 250,000 tons of Co2) have lower elasticities than the rest. 

6. Mapping Emission Reduction Under Different Policies.py creates interactive maps for the aforementioned scenarios. Each map (html format) shows individual plant-level response in specific census tracts to different policy scenarios.

# Visualizations
Note: This section includes a few of the important visualizations in the analysis. 

![PPs in California](Plant%20Mapping%20in%20California%20(Census%20Tract%20Level).png)
Fig. 1

This map shows all the fossil-fueled power plants in California by census tract. The pie chart for each power plant represents its unused capacity while the size of the charts shows the total generation potential. Blue color on the chart signifies unused capacity.

![PPs on tracts with income](Power%20Plants%20by%20Tracts%20with%20PPs%20and%20Income.png)
Fig. 2

This map shows just the census tracts with power plants in California. The tracts are heatmapped to represent income of the people living in the tract. 

![Top 5 tracts with highest emissions and potential with names](Top%205%20tracts%20with%20highest%20emissions%20and%20potential%20with%20names.png)
Fig. 3

This map shows the top 5 census tracts in California with the hgihest emissions and electricity generation potential. The power plants are named for identification purposes. 

![Plant nameplate capacity (MW)](res_Plant%20nameplate%20capacity%20(MW).png)
Fig. 4

This shows the spread of Plant nameplate capacity (MW) for all power plants in California using a historgram and a kernel density function.

![Census Tract Correlation Matrix](Census%20Tract%20Correlation%20Matrix.png)
Fig. 5

This is a correlation matrix for plant level data and census tract demographic information. The matrix could not locate a clear correlation between tract-level plant information and demographics of disadvantaged populations. 

![Dashboard Snapshot](Dashboard%20Snapshot.png)
Fig 6. A snapshot of an interactive map showing plant-level emission information pre and post permit-trading scenario. The simulation for this scenario was run on the assumption that bigger polluters (highlighted in yellow on the map) have higher elasticities than smaller polluters. This conception is based on the assumption that dirtier power plants have lower marginal abatement curves. 

The interactive maps for all the three possible scenarios need to be downloaded on desktop and opened in web browser:

a. Plant_Emission_Cmnd&Ctrl_Same_Elast_20%_Reduction

b. Plant_Emission_Permits_High_Elast_20%_Reduction shows the plant-level response to a permit trading scenario where bigger polluters have high elasticity.

c. Plant_Emission_Permits_Low_Elast_20%_Reduction shows the plant-level response to a permit trading scenario where bigger polluters have low elasticity.

As per the analysis, bigger polluters reduce more than smaller polluters if they have a higher elasticity of demand. And they perform better, in terms of reductions, under permit trading than command and control policy. However, bigger polluters reduce less if they have lower elasticities of demand. The location of each plant and emission-level information can be seen on the aforementioned interactive maps.


