# -*- coding: utf-8 -*-

"""
Preprocesses land use data and groups each lot into said lot group
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import cascaded_union
import shapefile
import geopy.distance

# Helper function to plot circle around coordinate point
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point

proj_wgs84 = pyproj.Proj(init='epsg:4326')

def geodesic_point_buffer(lat, lon, km):
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
        proj_wgs84)
    buf = Point(0, 0).buffer(km * 1000)  # distance in metres
    return transform(project, buf).exterior.coords[:]

print("STEP 0: Reading data")
# Import land use data
land_data_df = gpd.read_file("data/shape_files/Land_Use/land_use.shp")

# Create a dictionary of each land use c_dig2 to it's group type
zone_groups = {}
zone_groups[11] = 'Residential'
zone_groups[12] = 'Residential'
zone_groups[13] = 'Residential'
zone_groups[21] = 'Commercial'
zone_groups[22] = 'Commercial'
zone_groups[23] = 'Commercial'
zone_groups[31] = 'Industrial'
zone_groups[41] = 'Civic/Inst'
zone_groups[51] = 'Transportation'
zone_groups[52] = 'Transportation'
zone_groups[61] = 'Cultural/Park'
zone_groups[62] = 'Cultural/Park'
zone_groups[71] = 'Cultural/Park'
zone_groups[72] = 'Cultural/Park'
zone_groups[81] = 'Water'
zone_groups[91] = 'Vacant'
zone_groups[92] = 'Other/Unknown'

# Aggregate the polygons in each zone together
print("STEP 1: Aggregating Polygons in zones together")
land_data_df['zone'] = land_data_df.apply(lambda row: zone_groups[row.c_dig2], axis=1)
land_data_df_core = land_data_df[['zone', 'geometry']]

df_geometry_list = land_data_df_core.groupby('zone')['geometry'].apply(list).reset_index(name='geometries')
df_geometry_list['counts'] = df_geometry_list.apply(lambda row: len(row.geometries), axis=1)

for index, row in df_geometry_list.iterrows():
    print(row.zone)    
    row['merged_geometry'] = cascaded_union(row.geometries)

# Import basic lots data
print("STEP 2: Assigning land areas to greened lots")
greened_lots_df = pd.read_csv("data/raw_data/greened_lots.csv")
greened_lots_df_core = greened_lots_df[['id', 'lon', 'lat']]

zone_index = 1

for zone_index in range(df_geometry_list.zone.count()):    
    zone_name = df_geometry_list.iloc[zone_index].zone
    print(zone_name)
    zone_shape = df_geometry_list.iloc[zone_index].merged_geometry
    zone_areas = []    
    # Iterate through lots and append the necessary 
    for lot_index, lot_row in greened_lots_df_core.iterrows():
        if lot_index % 100 == 0:
            print(lot_index)
        radius = Polygon(geodesic_point_buffer(lot_row.lat, lot_row.lon, .2))        
        try:
            zone_areas.append(radius.intersection(zone_shape).area)
        except:
            zone_areas.append(0)
    greened_lots_df_core[zone_name] = zone_areas
    
greened_lots_df_core.to_csv("data/processed_data/greened_lots_with_land_use.csv")
    
    