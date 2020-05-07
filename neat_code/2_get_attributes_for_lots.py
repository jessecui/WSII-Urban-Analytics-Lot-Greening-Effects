#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 00:29:01 2020

This data creates a full attributes dataset for each lot. However,
the bulk of this code assumes the dataset has already been made. The code
to create this is in the archived_old_code folder, which was code I made
in the fall semester of 2019.

Refer to final_preprocessor_part_1.py and final_preprocessor_part_2.py in the 
archived_old_code section to learn how to get the full attributes dataset. 

To learn how to get the land zoning use attributes data,
also refer to land_preprocessor_part_1.py, land_preprocessor_part_2.py,
and land_preprocessor_part_3.py in the archived_old_code section.


@author: jessecui
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, shape
import shapefile

greened_attr_all_df = pd.read_csv("../neat_data/processed_data/greened_lots_attributes_all.csv")
greened_rel_df = pd.read_csv("../neat_data/cleaned_data/cleaned_greened_lots.csv")

greened_attr_df = greened_attr_all_df[greened_attr_all_df.id.isin(greened_rel_df.id)].copy()
greened_attr_df = greened_attr_df.reset_index()
greened_attr_df['date_season_begin'] = greened_rel_df['date_season_begin']
greened_attr_df = greened_attr_df.drop("index", axis=1)

greened_attr_df.to_csv("../neat_data/processed_data/greened_lots_attr.csv", index=False)

# Vacant lots is a little harder- we have to pull all vacant data again and 
# fill in missing values with the value of its duplicate
vacant_attr_all_df = pd.read_csv("../neat_data/processed_data/vacant_lots_attributes_all.csv")
vacant_rel_df = pd.read_csv("../neat_data/cleaned_data/cleaned_vacant_lots.csv")

viol_df = pd.read_csv("../neat_data/raw_data/li_violations.csv")
viol_df = viol_df[viol_df['violationdescription'].str.contains("VACANT LOT") == True]

# Join with available data
viol_df = viol_df[['objectid', 'address']]

vacant_attr_all_df = vacant_attr_all_df.sort_values('objectid') 

merged_viol_df = viol_df.merge(vacant_attr_all_df, how='left', on='objectid')

viol_df_filled = merged_viol_df.sort_values('address')\
          .groupby('address').apply(lambda x: x.ffill().bfill())\
          .drop_duplicates()
          
vacant_attr_df = viol_df_filled[viol_df_filled.objectid.isin(vacant_rel_df.objectid)]
vacant_attr_df = vacant_attr_df.drop('address', axis=1)
vacant_attr_df = vacant_attr_df.dropna()

# Save data

vacant_attr_df.to_csv("../neat_data/processed_data/vacant_lots_attr.csv", index=False)

# _----- APPENDING ECONOMIC DATA
# I forgot to include income to poverty data beforehand, so I will include them here now
poverty_df = pd.read_csv("../neat_data/raw_data/economic_poverty_data.csv")
poverty_df = poverty_df.iloc[1:]

poverty_df["income_to_poverty_under_.50"] = poverty_df.HD01_VD02.astype('int64') / poverty_df.HD01_VD01.astype('int64')
poverty_df["income_to_poverty_.50_to_.99"] = poverty_df.HD01_VD03.astype('int64') / poverty_df.HD01_VD01.astype('int64')
poverty_df["income_to_poverty_1.00_to_1.24"] = poverty_df.HD01_VD04.astype('int64') / poverty_df.HD01_VD01.astype('int64')
poverty_df["income_to_poverty_1.25_to_1.49"] = poverty_df.HD01_VD05.astype('int64') / poverty_df.HD01_VD01.astype('int64')
poverty_df["income_to_poverty_1.50_to_1.84"] = poverty_df.HD01_VD06.astype('int64') / poverty_df.HD01_VD01.astype('int64')
poverty_df["income_to_poverty_1.85_to_1.99"] = poverty_df.HD01_VD07.astype('int64') / poverty_df.HD01_VD01.astype('int64')
poverty_df["income_to_poverty_over_2.00"] = poverty_df.HD01_VD08.astype('int64') / poverty_df.HD01_VD01.astype('int64')

# Keep the relevant columns
poverty_df = poverty_df.iloc[:, [1, 19, 20, 21, 22, 23, 24, 25]]
poverty_df.fillna(0)

# Get the census block per lot
greened_attr_df = pd.read_csv("../neat_data/processed_data/greened_lots_attr.csv")
vacant_attr_df = pd.read_csv("../neat_data/processed_data/vacant_lots_attr.csv")

greened_lots_df = pd.read_csv("../neat_data/cleaned_data/cleaned_greened_lots.csv")
vacant_lots_df = pd.read_csv("../neat_data/cleaned_data/cleaned_vacant_lots.csv")

# Get the block groups for the greened and vacant lots
# Import census block files
shp = shapefile.Reader("../neat_data/Census_Block_Groups/Census_Block_Groups_2010.shp")
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
greened_lots_df.to_csv("../neat_data/processed_data/greened_lots_with_block.csv")
    
# Repeat steps but with vacant lots
# Parse vacant lots dataset
vacant_lots_groups = []

for lot_index, lot_row in vacant_lots_df.iterrows():
    if lot_index % 100 == 0:
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
vacant_lots_df.to_csv("../neat_data/processed_data/vacant_lots_with_block.csv")

# Now join the lots df to the income to poverty data by block id
greened_lots_with_poverty_df = pd.merge(greened_lots_df, poverty_df, left_on="census_block_index", right_on="GEO.id2")
greened_lots_with_poverty_df = greened_lots_with_poverty_df.iloc[:, [1, 7, 8, 9, 10, 11, 12, 13]]

vacant_lots_with_poverty_df = pd.merge(vacant_lots_df, poverty_df, left_on="census_block_index", right_on="GEO.id2")
vacant_lots_with_poverty_df = vacant_lots_with_poverty_df.iloc[:, [1, 7, 8, 9, 10, 11, 12, 13]]

# Now join the attributes df to the poverty data df by lot
greened_lots_attr_new = pd.merge(greened_attr_df, greened_lots_with_poverty_df, on="id")
greened_lots_attr_new.to_csv("../neat_data/processed_data/greened_lots_attr_new.csv", index=False)

vacant_lots_attr_new = pd.merge(vacant_attr_df, vacant_lots_with_poverty_df, on="objectid")
vacant_lots_attr_new.to_csv("../neat_data/processed_data/vacant_lots_attr_new.csv", index=False)
