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
crime_df = crime_df[['dispatch_date', 'lat', 'lng', 'ucr_general']]

# Drop all rows with NANs
crime_df = crime_df.dropna()

# Make sure crime data has date time settings for its date
crime_df['dispatch_date'] = pd.to_datetime(crime_df['dispatch_date'])

# Make sure lots data has date time settings for its date
greened_lots_df['date_season_begin'] = pd.to_datetime(greened_lots_df['date_season_begin'])
greened_lots_df = greened_lots_df[pd.notnull(greened_lots_df['date_season_begin'])] # Parse out all null entries

vacant_lots_df['violationdate'] = pd.to_datetime(vacant_lots_df['violationdate'])
vacant_lots_df = vacant_lots_df[pd.notnull(vacant_lots_df['violationdate'])] # Parse out all null entries

# Partition crime by year
datasets_year = {}
for year in range(2006, 2020):
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    crime_df_year = crime_df[(crime_df['dispatch_date'] < pd.Timestamp(end)) & 
                                 (crime_df['dispatch_date'] > pd.Timestamp(start))]    
    datasets_year[year] = crime_df_year
    
    print(year, ": ", crime_df_year.shape[0])

crime_100_meters_before = []
crime_100_meters_after = []

# Loop through the index data 
for lot_index, lot_row in greened_lots_df.iterrows():
    print("LOT INDEX: ", lot_index)
        
    # Initialize arrays for tracking crimes before and after greening intervention
    crimes_for_lot_before = []
    crimes_for_lot_after = []
    
    point = Point(lot_row.lon, lot_row.lat)
    
    # Subset dataset on date    
    lot_date = lot_row.date_season_begin.date()
    lot_date_upper = pd.Timestamp(lot_date + datetime.timedelta(days=365))
    lot_date_lower = pd.Timestamp(lot_date - datetime.timedelta(days=365))
    
    # Find the correct year set
    if lot_date.year == 2019:
        year_df = datasets_year[lot_date.year]        
    elif lot_date.year >= 2006:
        year_df = datasets_year[lot_date.year].append(datasets_year[lot_date.year + 1])
    else:
        crime_100_meters_before.append(-1)
        crime_100_meters_after.append(-1)              
        
    # Subset on the date range
    rel_crimes_df = year_df[(year_df['dispatch_date'] < lot_date_upper) & 
                                 (year_df['dispatch_date'] > lot_date_lower)]  
    
    rel_crimes_df = rel_crimes_df.reset_index()
    
    lot_coord = (lot_row.lon, lot_row.lat)

    # Loop through all crime data and append if the crime is within the 
    # date range and time range of the data
    for crime_index, crime_row in rel_crimes_df.iterrows():
        if crime_index % 10000 == 0:
            print("CRIME INDEX: ", crime_index)        
        crime_coord = (crime_row.lng, crime_row.lat)
        try:
            if geopy.distance.distance(lot_coord, crime_coord).meters < 100:
                if crime_row.dispatch_date < lot_row.date_season_begin:
                    crimes_for_lot_before.append(crime_row.ucr_general)
                else:
                    crimes_for_lot_after.append(crime_row.ucr_general)
        except:
            pass
            #print("CRIME PARSE ERROR 100 METERS")
    crime_100_meters_before.append(crimes_for_lot_before)
    crime_100_meters_after.append(crimes_for_lot_after)
        
        
        


geopy.distance.vincenty(coords_1, coords_2).meters

viol_date