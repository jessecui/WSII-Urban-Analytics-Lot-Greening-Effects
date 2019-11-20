#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Appends crime data to lots data based on distance and time

@author: jessecui
"""
import geopy.distance
import pandas as pd
from shapely.geometry import Point, Polygon, shape
import datetime
import numpy as np

def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (datetime.date(d.year + years, 1, 1) - datetime.date(d.year, 1, 1))

# Import Data
print("STEP 1: Import Data")
crime_df = pd.read_csv("data/raw_data/crime.csv")
greened_lots_df = pd.read_csv("data/processed_data/greened_lots_with_block.csv")
vacant_lots_df = pd.read_csv("data/processed_data/vacant_lots_with_block.csv")

# Preprocess the crimes to drop all unnecessary columns
crime_df = crime_df[['dispatch_date', 'lat', 'lng', 'ucr_general', 'text_general_code']]

# Drop all rows with NANs
crime_df = crime_df.dropna()

# Make sure crime data has date time settings for its date
crime_df['dispatch_date'] = pd.to_datetime(crime_df['dispatch_date'])

# Make sure lots data has date time settings for its date
greened_lots_df['date_season_begin'] = pd.to_datetime(greened_lots_df['date_season_begin'])
greened_lots_df = greened_lots_df[pd.notnull(greened_lots_df['date_season_begin'])] # Parse out all null entries

crime_100_meters_before = []
crime_100_meters_after = []
crime_200_meters_before = []
crime_200_meters_after = []
crime_500_meters_before = []
crime_500_meters_after = []

print("STEP 2: Determine crimes per lot")
# Loop through the index data 
for lot_index, lot_row in greened_lots_df.iterrows():
    print("LOT INDEX: ", lot_index)
        
    # Initialize arrays for tracking crimes before and after greening intervention
    crimes_100_for_lot_before = []
    crimes_100_for_lot_after = []
    crimes_200_for_lot_before = []
    crimes_200_for_lot_after = []
    crimes_500_for_lot_before = []
    crimes_500_for_lot_after = []
    
    point = Point(lot_row.lon, lot_row.lat)
    
    # Subset dataset on date    
    lot_date = lot_row.date_season_begin.date()
    lot_date_upper = pd.Timestamp(lot_date + datetime.timedelta(days=365))
    lot_date_lower = pd.Timestamp(lot_date - datetime.timedelta(days=365))
    
    # Find the correct year set
    #if lot_date.year == 2019:
    #    year_df = datasets_year[lot_date.year]        
    #elif lot_date.year >= 2006:
    #    year_df = datasets_year[lot_date.year].append(datasets_year[lot_date.year + 1])
    #else:
    #    crime_100_meters_before.append(-1)
    #    crime_100_meters_after.append(-1)              
        
    # Subset on the date range
    lot_coord = (lot_row.lon, lot_row.lat)
    rel_crimes_df = crime_df[(crime_df['lat'] < lot_row.lat + 0.02) & (crime_df['lat'] > lot_row.lat - 0.02) & #approx 500 meters radius
                             (crime_df['lng'] < lot_row.lon + 0.005) & (crime_df['lng'] > lot_row.lon - 0.005) & #approx 500 meters radius
                             (crime_df['dispatch_date'] < lot_date_upper) & 
                             (crime_df['dispatch_date'] > lot_date_lower)]      
    print("SIZE: ", rel_crimes_df.shape[0])
    rel_crimes_df = rel_crimes_df.reset_index()

    # Loop through all crime data and append if the crime is within the 
    # date range and time range of the data
    for crime_index, crime_row in rel_crimes_df.iterrows():
        if crime_index % 1000 == 0:
            print("CRIME INDEX: ", crime_index)        
        crime_coord = (crime_row.lng, crime_row.lat)
        # 100 Meters
        try:
            if geopy.distance.distance(lot_coord, crime_coord).meters < 100:
                if crime_row.dispatch_date < lot_row.date_season_begin:
                    crimes_100_for_lot_before.append(crime_row.ucr_general)
                else:
                    crimes_100_for_lot_after.append(crime_row.ucr_general)
        except:
            pass
        
        # 200 Meters
        try:
            if geopy.distance.distance(lot_coord, crime_coord).meters < 200:
                if crime_row.dispatch_date < lot_row.date_season_begin:
                    crimes_200_for_lot_before.append(crime_row.ucr_general)
                else:
                    crimes_200_for_lot_after.append(crime_row.ucr_general)
        except:
            pass

        # 500 Meters
        try:
            if geopy.distance.distance(lot_coord, crime_coord).meters < 500:
                if crime_row.dispatch_date < lot_row.date_season_begin:
                    crimes_500_for_lot_before.append(crime_row.ucr_general)
                else:
                    crimes_500_for_lot_after.append(crime_row.ucr_general)
        except:
            pass        
        
    crime_100_meters_before.append(crimes_100_for_lot_before)
    crime_100_meters_after.append(crimes_100_for_lot_after)
    crime_200_meters_before.append(crimes_200_for_lot_before)
    crime_200_meters_after.append(crimes_200_for_lot_after)
    crime_500_meters_before.append(crimes_500_for_lot_before)
    crime_500_meters_after.append(crimes_500_for_lot_after)
    
greened_lots_df["100_before"] = crime_100_meters_before
greened_lots_df["100_after"] = crime_100_meters_after
greened_lots_df["200_before"] = crime_200_meters_before
greened_lots_df["200_after"] = crime_200_meters_after
greened_lots_df["500_before"] = crime_500_meters_before
greened_lots_df["500_after"] = crime_500_meters_after
    
greened_lots_df.to_csv("data/processed_data/processed_greened_lots_with_crimes.csv")
    
#geopy.distance.distance((-75.150, 40.05), (-75.151, 40.05)).meters