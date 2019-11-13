# -*- coding: utf-8 -*-

"""
Consolidates land use plots into specified groups (and also merges them)
"""

import geopandas as gpd
from shapely.ops import cascaded_union
import pickle

print("STEP 1: Reading data")
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
print("STEP 2: Aggregating Polygons in zones together")
land_data_df['zone'] = land_data_df.apply(lambda row: zone_groups[row.c_dig2], axis=1)
land_data_df_core = land_data_df[['zone', 'geometry']]

df_geometry_list = land_data_df_core.groupby('zone')['geometry'].apply(list).reset_index(name='geometries')
df_geometry_list['counts'] = df_geometry_list.apply(lambda row: len(row.geometries), axis=1)

print(df_geometry_list[['zone', 'counts']])

print("STEP 3: Cascade Unioning the Zones Together (except Residential)")
for index, row in df_geometry_list.iterrows():
    if index != 6:
        continue    
    else:    
        print(row.zone)    
        unioned_data = cascaded_union(row.geometries)
        file_string = "data/processed_data/Land_Use/Land_Categories/merged_"+row.zone[:3]+str(index)+"_shape.pickle"
        with open(file_string , 'wb') as handle:
            pickle.dump(unioned_data , handle, protocol=pickle.HIGHEST_PROTOCOL)



print("STEP 4: Cascade Unioning the Zones Together (just Residential)")
