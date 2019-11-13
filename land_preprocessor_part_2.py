#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 22:20:47 2019

@author: jessecui

Finds the areas of land use plot types for each vacant/greened lot
"""

import pandas as pd
from shapely import wkt

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
print("STEP 2: Assigning land areas to greened lots")
df_geometry_list = pd.read_csv("data/processed_data/geometry_list_1.csv")
greened_lots_df = pd.read_csv("data/raw_data/greened_lots.csv")
greened_lots_df_core = greened_lots_df[['id', 'lon', 'lat']]

for zone_index in range(df_geometry_list.zone.count()):        
    zone_name = df_geometry_list.iloc[zone_index].zone    
    print(zone_name)
    if zone_name == 'Residential':
        continue
    zone_shape = wkt.loads(df_geometry_list.iloc[zone_index].merged_geometry)
    zone_areas = []    
    # Iterate through lots and append the necessary 
    for lot_index, lot_row in greened_lots_df_core.iterrows():
        if lot_index % 50 == 0:
            print(zone_name, ': ', lot_index)
        radius = Polygon(geodesic_point_buffer(lot_row.lat, lot_row.lon, .2))        
        try:
            zone_areas.append(radius.intersection(zone_shape).area)
        except:
            print("INTERSECTION ERROR")
            zone_areas.append(0)
    greened_lots_df_core[zone_name] = zone_areas
    
greened_lots_df_core.to_csv("data/processed_data/greened_lots_with_land_use.csv")
    