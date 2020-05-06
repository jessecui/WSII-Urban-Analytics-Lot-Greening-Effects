#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:53:07 2020

Appends crime data to vacant lots data based on distance and time
Uses the average greening date at the control date.

@author: jessecui
"""

import geopy.distance
import pandas as pd
from shapely.geometry import Point, Polygon, shape
import datetime
import numpy as np
import functools
import operator

def avg_datetime(series):
    dt_min = series.min()
    deltas = [x-dt_min for x in series]
    return dt_min + functools.reduce(operator.add, deltas) / len(deltas)

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
crime_df = pd.read_csv("../neat_data/cleaned_data/cleaned_crimes.csv")
greened_lots_df = pd.read_csv("../neat_data/cleaned_data/cleaned_greened_lots.csv")
vacant_lots_df = pd.read_csv("../neat_data/cleaned_data/cleaned_vacant_lots.csv")

print("STEP 2 : Prepare Data")

# Preprocess the crimes to drop all unnecessary columns
crime_df = crime_df[['dispatch_date', 'lat', 'lng', 'ucr_general', 'text_general_code']]

# Drop all rows with NANs
crime_df = crime_df.dropna()

# Drop all crimes that aren't relevant
relevant_codes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1400, 2000, 2300, 2400, 2500]
crime_df = crime_df[crime_df['ucr_general'].isin(relevant_codes)]

# Drop the recovered stolen vehicles section
crime_df = crime_df[crime_df['text_general_code'] != "Recovered Stolen Motor Vehicle"]

# Make sure crime data has date time settings for its date
crime_df['dispatch_date'] = pd.to_datetime(crime_df['dispatch_date'])

# Make sure lots data has date time settings for its date
greened_lots_df['date_season_begin'] = pd.to_datetime(greened_lots_df['date_season_begin'])
greened_lots_df = greened_lots_df[pd.notnull(greened_lots_df['date_season_begin'])] # Parse out all null entries
greened_lots_df = greened_lots_df.dropna(subset=['date_season_begin'])

# Take all greened lots in the crime range
greened_lots_df = greened_lots_df[(greened_lots_df['date_season_begin'] >= crime_df.dispatch_date.min()) & (greened_lots_df['date_season_begin'] <= crime_df.dispatch_date.max())]

# Find the average greened lots intervention time
avg_date = pd.Timestamp((greened_lots_df.date_season_begin - greened_lots_df.date_season_begin.min()).mean() + greened_lots_df.date_season_begin.min())

avg_date_upper_start = pd.Timestamp(avg_date + datetime.timedelta(days=180))
avg_date_upper_end = pd.Timestamp(avg_date + datetime.timedelta(days=545))
avg_date_lower_start = pd.Timestamp(avg_date - datetime.timedelta(days=545))
avg_date_lower_end = pd.Timestamp(avg_date - datetime.timedelta(days=180))

# Only take the relevant interval
crime_df = crime_df[(((crime_df['dispatch_date'] >= avg_date_upper_start) & (crime_df['dispatch_date'] <= avg_date_upper_end)) | # 6-18 month after
                         ((crime_df['dispatch_date'] >= avg_date_lower_start) & (crime_df['dispatch_date'] <= avg_date_lower_end)))] #6-18 month before


# Preprocess the vacant lots data

crime_100_meters_before = []
crime_100_meters_after = []
crime_200_meters_before = []
crime_200_meters_after = []
crime_500_meters_before = []
crime_500_meters_after = []

print("STEP 3: Determine crimes per lot")
# Loop through the index data 
for lot_index, lot_row in vacant_lots_df.iterrows():
    print("LOT INDEX: ", lot_index)
        
    # Initialize arrays for tracking crimes before and after greening intervention
    crimes_100_for_lot_before = []
    crimes_100_for_lot_after = []
    crimes_200_for_lot_before = []
    crimes_200_for_lot_after = []
    crimes_500_for_lot_before = []
    crimes_500_for_lot_after = []
        
    # Subset on the date range
    lot_coord = (lot_row.lng, lot_row.lat)
    rel_crimes_df = crime_df[(crime_df['lat'] < lot_row.lat + 0.02) & (crime_df['lat'] > lot_row.lat - 0.02) & #approx 500 meters radius
                             (crime_df['lng'] < lot_row.lng + 0.005) & (crime_df['lng'] > lot_row.lng - 0.005)] #approx 500 meters radius
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
    
vacant_lots_df["100_before"] = crime_100_meters_before
vacant_lots_df["100_after"] = crime_100_meters_after
vacant_lots_df["200_before"] = crime_200_meters_before
vacant_lots_df["200_after"] = crime_200_meters_after
vacant_lots_df["500_before"] = crime_500_meters_before
vacant_lots_df["500_after"] = crime_500_meters_after
    
vacant_lots_df.to_csv("../neat_data/processed_data/vacant_lots_unmatched_crimes.csv")