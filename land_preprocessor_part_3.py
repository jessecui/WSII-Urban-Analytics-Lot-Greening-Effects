#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 22:20:47 2019

@author: jessecui

Finds the areas of land use plot types for each vacant lot
"""

import pandas as pd
from shapely import wkt
import pickle    

# Helper function to plot circle around coordinate point
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Polygon
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

# Import basic lots data
print("STEP 1: Assigning land areas to vacant lots")
df_geometry_list = pd.read_csv("data/processed_data/Land_Use/Land_Categories/zone_geometry_final.csv")
vacant_lots_df = pd.read_csv("data/raw_data/vacant_lots.csv")
vacant_lots_df_core = vacant_lots_df[['objectid', 'lng', 'lat']]

# Loop through the list of data for merged zones and find the areas
for zone_index in range(df_geometry_list.zone.count()):
    zone_name = df_geometry_list.iloc[zone_index].zone    
    print(zone_name)
    zone_shape = wkt.loads(df_geometry_list.iloc[zone_index].geometry)
    zone_areas = []    
    # Iterate through lots and append the necessary 
    for lot_index, lot_row in vacant_lots_df_core.iterrows():
        if lot_index % 10 == 0:
            print(zone_name, ': ', lot_index)                    
        try:
            radius = Polygon(geodesic_point_buffer(lot_row.lat, lot_row.lng, .2))
            zone_areas.append(radius.intersection(zone_shape).area)
        except:
            print("INTERSECTION ERROR")
            zone_areas.append(-1)
    file_string = "data/processed_data/Land_Use/Lot_Proportions/vacant_areas_"+zone_name[:3]+str(zone_index)+".pickle"
    with open(file_string , 'wb') as handle:
        pickle.dump(zone_areas, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
#greened_lots_df_core.to_csv("data/processed_data/greened_lots_with_land_use.csv")
    