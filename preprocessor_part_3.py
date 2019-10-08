#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Appends crime data to lots data based on distance and time

@author: jessecui
"""
import geopy.distance
import pandas as pd

# Import Data
crime_df = pd.read_csv("data/crime.csv")
greened_lots_df = pd.read_csv("data/greened_lots_with_block.csv")
vacant_lots_df = pd.read_csv("data/vacant_lots_with_block.csv")

# Make sure crime data has date time
crime_df['dispatch_date'] = pd.to_datetime(crime_df['dispatch_date'])

100_meters_crime = []

# Loop through greened lots
for lot_index, lot_row in greened_lots_df.iterrows():
    if lot_index % 10 == 0:
        print(lot_index) 


geopy.distance.vincenty(coords_1, coords_2).km