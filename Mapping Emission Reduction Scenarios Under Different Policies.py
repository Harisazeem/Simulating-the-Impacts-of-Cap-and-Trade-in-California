import geopandas as gpd
import pandas as pd
import folium

# Load census tracts from GeoPackage
tracts = gpd.read_file("Tract_Demo_AllTracts.gpkg")
tracts['poc_pop_ratio'] = tracts['poc_pop'] / tracts['tot_pop']


####An Interactive Map for Permit Trading Scenario with bigger polluters having high elasticities####
# Load powerplant data from CSV
plants = pd.read_csv("Plant_prmt_high_elast.csv")

# Convert the powerplant DataFrame to a GeoDataFrame
geometry = gpd.points_from_xy(plants.longitude, plants.latitude)
plants_gdf = gpd.GeoDataFrame(plants, geometry=geometry, crs="EPSG:4326")

# Define colors based on emissions
plants_gdf['color'] = 'green'  # default color
plants_gdf.loc[plants_gdf['Plant annual CO2 equivalent emissions (tons)'] > 250000, 'color'] = 'yellow'

# Define marker size based on 'prct_change_permits with 20.0% reduction' column
plants_gdf['marker_size'] = 10  # default size
plants_gdf.loc[plants_gdf['prct_change_permits with 20.0% reduction'] < -11.0, 'marker_size'] = 20

# Create a map centered on California without any base map
m = folium.Map(location=[36.7783, -119.4179], zoom_start=6, tiles=None)

# Add census tracts to the map with finer boundaries
folium.GeoJson(tracts, style_function=lambda feature: {'color': 'black', 'weight': 0.5}).add_to(m)

# Add powerplant locations with color and size coding
for idx, row in plants_gdf.iterrows():
    popup_text = f"<b>Plant Name:</b> {row['Plant name']}<br>"
    popup_text += f"<b>Annual Emissions (tons):</b> {row['Plant annual CO2 equivalent emissions (tons)']}<br>"
    popup_text += f"<b>Permits Post Reduction:</b> {row['permits_post_reduction']}<br>"
    popup_text += f"<b>Prct Change Permits with 20.0% Reduction:</b> {row['prct_change_permits with 20.0% reduction']}<br>"
    
    folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=row['marker_size'],
                        fill=True, color='black', fill_opacity=1, popup=popup_text, 
                        fill_color=row['color'], weight=1).add_to(m)  # Adding black border

# Add legend for color
color_legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index:9999; font-size:14px; background-color:white; border-radius:5px; padding:10px;">
        <b>Color Legend:</b><br>
        <span style="color: green;">◉</span> Annual Emissions < 250,000 tons<br>
        <span style="color: yellow;">◉</span> Annual Emissions > 250,000 tons<br>
    </div>
'''
m.get_root().html.add_child(folium.Element(color_legend_html))

# Add legend for size
size_legend_html = '''
    <div style="position: fixed; bottom: 50px; right: 50px; z-index:9999; font-size:14px; background-color:white; border-radius:5px; padding:10px;">
        <b>Size Legend:</b><br>
        <span style="font-size:14px; color:#000000; line-height:0;">◉</span> Small reduction<br>
        <span style="font-size:20px; color:#000000; line-height:0;">◉</span> Large reduction<br>
    </div>
'''
m.get_root().html.add_child(folium.Element(size_legend_html))

# Save the map to an HTML file
m.save("Plant_Emission_Permits_High_Elast_20%_Reduction.html")

#%%
####An interactive Map for command & control scenario with all polluters having same elasticities####
# Load powerplant data from CSV
plants = pd.read_csv("Plant_prmt_cmmnd_ctrl.csv")

# Convert the powerplant DataFrame to a GeoDataFrame
geometry = gpd.points_from_xy(plants.longitude, plants.latitude)
plants_gdf = gpd.GeoDataFrame(plants, geometry=geometry, crs="EPSG:4326")

# Define colors based on emissions
plants_gdf['color'] = 'green'  # default color
plants_gdf.loc[plants_gdf['Plant annual CO2 equivalent emissions (tons)'] > 250000, 'color'] = 'yellow'

# Define marker size based on 'prct_change_permits with 20.0% reduction' column
plants_gdf['marker_size'] = 10  # default size


# Create a map centered on California without any base map
m = folium.Map(location=[36.7783, -119.4179], zoom_start=6, tiles=None)

# Add census tracts to the map with finer boundaries
folium.GeoJson(tracts, style_function=lambda feature: {'color': 'black', 'weight': 0.5}).add_to(m)

# Add powerplant locations with color and size coding
for idx, row in plants_gdf.iterrows():
    popup_text = f"<b>Plant Name:</b> {row['Plant name']}<br>"
    popup_text += f"<b>Annual Emissions (tons):</b> {row['Plant annual CO2 equivalent emissions (tons)']}<br>"
    popup_text += f"<b>Permits Post Reduction:</b> {row['permits_post_reduction']}<br>"
    popup_text += f"<b>Prct Change Permits with 20.0% Reduction:</b> {row['prct_change_permits with 20.0% reduction']}<br>"
    
    folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=row['marker_size'],
                        fill=True, color='black', fill_opacity=1, popup=popup_text, 
                        fill_color=row['color'], weight=1).add_to(m)  # Adding black border

# Add legend for color
color_legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index:9999; font-size:14px; background-color:white; border-radius:5px; padding:10px;">
        <b>Color Legend:</b><br>
        <span style="color: green;">◉</span> Annual Emissions < 250,000 tons<br>
        <span style="color: yellow;">◉</span> Annual Emissions > 250,000 tons<br>
    </div>
'''
m.get_root().html.add_child(folium.Element(color_legend_html))


# Save the map to an HTML file
m.save("Plant_Emission_Cmnd&Ctrl_Same_Elast_20%_Reduction.html")

#%%

####An interactive Map for Permit Trading Scenario with bigger polluters having lower elasticities####
# Load powerplant data from CSV
plants = pd.read_csv("Plant_prmt_low_elast.csv")

# Convert the powerplant DataFrame to a GeoDataFrame
geometry = gpd.points_from_xy(plants.longitude, plants.latitude)
plants_gdf = gpd.GeoDataFrame(plants, geometry=geometry, crs="EPSG:4326")

# Define colors based on emissions
plants_gdf['color'] = 'green'  # default color
plants_gdf.loc[plants_gdf['Plant annual CO2 equivalent emissions (tons)'] > 250000, 'color'] = 'yellow'

# Define marker size based on 'prct_change_permits with 20.0% reduction' column
plants_gdf['marker_size'] = 20  # default size
plants_gdf.loc[plants_gdf['prct_change_permits with 20.0% reduction'] > -30.0, 'marker_size'] = 10

# Create a map centered on California without any base map
m = folium.Map(location=[36.7783, -119.4179], zoom_start=6, tiles=None)

# Add census tracts to the map with finer boundaries
folium.GeoJson(tracts, style_function=lambda feature: {'color': 'black', 'weight': 0.5}).add_to(m)

# Add powerplant locations with color and size coding
for idx, row in plants_gdf.iterrows():
    popup_text = f"<b>Plant Name:</b> {row['Plant name']}<br>"
    popup_text += f"<b>Annual Emissions (tons):</b> {row['Plant annual CO2 equivalent emissions (tons)']}<br>"
    popup_text += f"<b>Permits Post Reduction:</b> {row['permits_post_reduction']}<br>"
    popup_text += f"<b>Prct Change Permits with 20.0% Reduction:</b> {row['prct_change_permits with 20.0% reduction']}<br>"
    
    folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=row['marker_size'],
                        fill=True, color='black', fill_opacity=1, popup=popup_text, 
                        fill_color=row['color'], weight=1).add_to(m)  # Adding black border

# Add legend for color
color_legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index:9999; font-size:14px; background-color:white; border-radius:5px; padding:10px;">
        <b>Color Legend:</b><br>
        <span style="color: green;">◉</span> Annual Emissions < 250,000 tons<br>
        <span style="color: yellow;">◉</span> Annual Emissions > 250,000 tons<br>
    </div>
'''
m.get_root().html.add_child(folium.Element(color_legend_html))

# Add legend for size
size_legend_html = '''
    <div style="position: fixed; bottom: 50px; right: 50px; z-index:9999; font-size:14px; background-color:white; border-radius:5px; padding:10px;">
        <b>Size Legend:</b><br>
        <span style="font-size:14px; color:#000000; line-height:0;">◉</span> Small reduction<br>
        <span style="font-size:20px; color:#000000; line-height:0;">◉</span> Large reduction<br>
    </div>
'''
m.get_root().html.add_child(folium.Element(size_legend_html))


# Save the map to an HTML file
m.save("Plant_Emission_Permits_Low_Elast_20%_Reduction.html")