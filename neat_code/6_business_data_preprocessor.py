#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code gets business characteristics per lot.

I.e. we get indicator variables to determine if a lot type is 
present within 200 meters surrounding a lot.

@author: jessecui
"""

import pandas as pd
import geopy.distance

# Read the data
business_df_hours = pd.read_csv("../neat_data/raw_data/business_frame_hours.csv")
business_df_no_hours = pd.read_csv("../neat_data/raw_data/business_frame_nohours.csv", encoding = "ISO-8859-1")

# Drop the hours data of the hours dataframe
columns_to_drop = business_df_hours.columns[13:181].append(business_df_hours.columns[184:187])
business_df_no_hours_2 = business_df_hours.drop(columns_to_drop, axis=1)

# Combine the data into one dataframe
business_df = pd.concat([business_df_no_hours, business_df_no_hours_2], ignore_index = True)

# Add the data to the attributes data for greened and vacant lots
greened_attr_df = pd.read_csv("../neat_data/processed_data/greened_lots_attr_new.csv")
vacant_attr_df = pd.read_csv("../neat_data/processed_data/vacant_lots_attr_new.csv")

# Retrieve the latitude and longitude data for each lot
greened_cleaned_df = pd.read_csv("../neat_data/cleaned_data/cleaned_greened_lots.csv")
vacant_cleaned_df = pd.read_csv("../neat_data/cleaned_data/cleaned_vacant_lots.csv")

greened_attr_with_coords_df = greened_attr_df.merge(greened_cleaned_df, on="id")
vacant_attr_with_coords_df = vacant_attr_df.merge(vacant_cleaned_df, on="objectid")

# Loop through the lots and determine the total number of businesses as well as the presence of each business type
greened_business_list = []
for lot_index, lot_row in greened_attr_with_coords_df.iterrows():
    if lot_index % 20 == 0:
        print("lot index: ", lot_index)
    
    bus_attr_list = [0] * 10
    lot_coord = (lot_row.lon, lot_row.lat)
    rel_bus_df = business_df[(business_df['lat'] < lot_row.lat + 0.01) & (business_df['lat'] > lot_row.lat - 0.01) & #approx 200 meters radius
                             (business_df['lng'] < lot_row.lon + 0.002) & (business_df['lng'] > lot_row.lon - 0.002)]#approx 200 meters radius
    
    # Subset the businesses that are within 200m of the lot
    business_count = 0
    for business_index, business_row in rel_bus_df.iterrows():
        business_coord = (business_row.lng, business_row.lat)
        
        # Create indicator variables for each business type as well as a total count of each type
        try:
            if geopy.distance.distance(lot_coord, business_coord).meters < 200:
                business_count += 1
                if business_row.cafe: bus_attr_list[0] = 1
                if business_row.convenience: bus_attr_list[1] = 1
                if business_row.gym: bus_attr_list[2] = 1
                if business_row.institution: bus_attr_list[3] = 1
                if business_row.liquor: bus_attr_list[4] = 1
                if business_row.lodging: bus_attr_list[5] = 1
                if business_row.nightlife: bus_attr_list[6] = 1
                if business_row.pharmacy: bus_attr_list[7] = 1
                if business_row.restaurant: bus_attr_list[8] = 1
                if business_row.retail: bus_attr_list[9] = 1
        except:
            print("ERROR ON DISTANCE PROCESSING")

            pass     
    new_df_row = [lot_row.id] + bus_attr_list + [business_count]
    greened_business_list.append(new_df_row)
    
greened_bus_attr_df = pd.DataFrame(greened_business_list, columns=["id","cafe","convenience","gym","institution","liquor","lodging","nightlife","pharmacy","restaurant","retail","business_count"])
greened_bus_attr_df.to_csv("../neat_data/processed_data/greened_lots_business_attr.csv")

# Do the same as the above for vacant lots
# Loop through the lots and determine the total number of businesses as well as the presence of each business type
vacant_business_list = []
for lot_index, lot_row in vacant_attr_with_coords_df.iterrows():
    if lot_index % 20 == 0:
        print("lot index: ", lot_index)
    
    bus_attr_list = [0] * 10
    lot_coord = (lot_row.lng, lot_row.lat)
    rel_bus_df = business_df[(business_df['lat'] < lot_row.lat + 0.01) & (business_df['lat'] > lot_row.lat - 0.01) & #approx 200 meters radius
                             (business_df['lng'] < lot_row.lng + 0.002) & (business_df['lng'] > lot_row.lng - 0.002)] #approx 200 meters radius
    
    # Subset the businesses that are within 200m of the lot
    business_count = 0
    for business_index, business_row in rel_bus_df.iterrows():
        business_coord = (business_row.lng, business_row.lat)
        
        # Create indicator variables for each business type as well as a total count of each type
        try:
            if geopy.distance.distance(lot_coord, business_coord).meters < 200:
                business_count += 1
                if business_row.cafe: bus_attr_list[0] = 1
                if business_row.convenience: bus_attr_list[1] = 1
                if business_row.gym: bus_attr_list[2] = 1
                if business_row.institution: bus_attr_list[3] = 1
                if business_row.liquor: bus_attr_list[4] = 1
                if business_row.lodging: bus_attr_list[5] = 1
                if business_row.nightlife: bus_attr_list[6] = 1
                if business_row.pharmacy: bus_attr_list[7] = 1
                if business_row.restaurant: bus_attr_list[8] = 1
                if business_row.retail: bus_attr_list[9] = 1
        except:
            print("ERROR ON DISTANCE PROCESSING")

            pass     
    new_df_row = [lot_row.objectid] + bus_attr_list + [business_count]
    vacant_business_list.append(new_df_row)
    
vacant_bus_attr_df = pd.DataFrame(vacant_business_list, columns=["objectid","cafe","convenience","gym","institution","liquor","lodging","nightlife","pharmacy","restaurant","retail","business_count"])
vacant_bus_attr_df.to_csv("../neat_data/processed_data/vacant_lots_business_attr.csv")

# Create a final dataframe that combines the business attributes with the rest of the attributes
greened_bus_attr_df = pd.read_csv("../neat_data/processed_data/greened_lots_business_attr.csv")
greened_bus_attr_df.drop(greened_bus_attr_df.columns[0], axis=1)
greened_attr_with_business_df = pd.concat([greened_attr_df, greened_bus_attr_df.iloc[:,1:]], axis=1)
greened_attr_with_business_df.to_csv("../neat_data/processed_data/greened_attr_with_business_new.csv")

vacant_bus_attr_df = pd.read_csv("../neat_data/processed_data/vacant_lots_business_attr.csv")
vacant_bus_attr_df.drop(vacant_bus_attr_df.columns[0], axis=1)
vacant_attr_with_business_df = pd.concat([vacant_attr_df, vacant_bus_attr_df.iloc[:,1:]], axis=1)
vacant_attr_with_business_df.to_csv("../neat_data/processed_data/vacant_attr_with_business_new.csv")