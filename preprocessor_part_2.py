# Import shape files data from Census Bureau data and clean them

import pandas as pd

# Import basic crime data
crime_df = pd.read_csv("data/crime.csv")
greened_lots_df = pd.read_csv("data/greened_lots.csv")
vacant_lots_df = pd.read_csv("data/vacant_lots.csv")

import geopandas as gpd
from shapely.geometry import Point, Polygon

# Import census block files
census_data = gpd.read_file("data/shape_files/Census_Block_Groups/Census_Block_Groups_2010.shp")
census_data_head = census_data.head()

# Loop through the lots datasets
# For each entry, determine which block group it's coordinates lie in

# Parse greened lots dataset
greened_lots_groups = []

for lot_index, lot_row in greened_lots_df.iterrows():
    if lot_index % 10 == 0:
        print(lot_index)    
    point = Point(lot_row.lon, lot_row.lat)
    found_block = False
    for census_index, census_row in census_data.iterrows():
        if census_row.geometry.contains(point):
            group = int(census_row.BLKGRPCE10)
            greened_lots_groups.append(group)
            found_block = True
            break
    if not found_block:
        greened_lots_groups.append(-1)
        print("BLOCK NOT FOUND")
        
# Attach the blocks column to the dataset        
greened_lots_df["census_block"] = greened_lots_groups
greened_lots_df.to_csv("data/greened_lots_with_block.csv")
    
# Repeat steps but with vacant lots
# Parse vacant lots dataset
vacant_lots_groups = []

for lot_index, lot_row in vacant_lots_df.iterrows():
    if lot_index % 10 == 0:
        print(lot_index)    
    point = Point(lot_row.lng, lot_row.lat)
    found_block = False
    for census_index, census_row in census_data.iterrows():
        if census_row.geometry.contains(point):
            group = int(census_row.BLKGRPCE10)
            vacant_lots_groups.append(group)
            found_block = True
            break
    if not found_block:
        vacant_lots_groups.append(-1)
        print("BLOCK NOT FOUND")
        
# Attach the blocks column to the dataset        
vacant_lots_df["census_block"] = vacant_lots_groups
vacant_lots_df.to_csv("data/vacant_lots_with_block.csv")
    