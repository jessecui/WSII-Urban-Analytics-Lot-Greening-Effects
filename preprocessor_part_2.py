#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import shape files data from Census Bureau data and clean them

@author: jessecui
"""


import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, shape
import shapefile

# Import basic crime data
greened_lots_df = pd.read_csv("data/raw_data/greened_lots.csv")
vacant_lots_df = pd.read_csv("data/raw_data/vacant_lots.csv")

# Import census block files
census_data = gpd.read_file("data/shape_files/Census_Block_Groups/Census_Block_Groups_2010.shp")
census_data_head = census_data.head()

shp = shapefile.Reader("data/shape_files/Census_Block_Groups/Census_Block_Groups_2010.shp")
all_shapes = shp.shapes()
all_records = shp.records()

# Loop through the lots datasets
# For each entry, determine which block group it's coordinates lie in

# Parse greened lots dataset
greened_lots_groups = []

for lot_index, lot_row in greened_lots_df.iterrows():
    if lot_index % 100 == 0:
        print(lot_index)    
    point = Point(lot_row.lon, lot_row.lat)    
    found_block = False
    for i in range(len(all_shapes)):
        boundary = all_shapes[i] # get a boundary polygon
        if point.within(shape(boundary)): # make a point and see if it's in the polygon
            greened_lots_groups.append(all_records[i][5])
            found_block = True
            break
    if not found_block:
        greened_lots_groups.append(-1)
        print("BLOCK NOT FOUND")
        
# Attach the blocks column to the dataset        
greened_lots_df["census_block_index"] = greened_lots_groups
greened_lots_df.to_csv("data/processed_data/greened_lots_with_block.csv")
    
# Repeat steps but with vacant lots
# Parse vacant lots dataset
vacant_lots_groups = []

for lot_index, lot_row in vacant_lots_df.iterrows():
    if lot_index % 10 == 0:
        print(lot_index)    
    point = Point(lot_row.lng, lot_row.lat)
    found_block = False
    for i in range(len(all_shapes)):
        boundary = all_shapes[i] # get a boundary polygon
        if point.within(shape(boundary)): # make a point and see if it's in the polygon
            vacant_lots_groups.append(all_records[i][5])
            found_block = True
            break
    if not found_block:
        vacant_lots_groups.append(-1)
        print("BLOCK NOT FOUND")
        
# Attach the blocks column to the dataset        
vacant_lots_df["census_block_index"] = vacant_lots_groups
vacant_lots_df.to_csv("data/processed_data/vacant_lots_with_block.csv")
    