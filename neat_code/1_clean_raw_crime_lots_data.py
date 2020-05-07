#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 19:13:36 2020

Cleans the raw data for greened lots, vacant lots, and crimes and creates
new cleaned datasets for each.

@author: jessecui
"""

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from shapely.ops import cascaded_union
from shapely.geometry import MultiPolygon
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import intersects

# Clean the greened lots data
# Only include lots that were greened between 9/01/2007 - 09/01/2017
greened_lots_df = pd.read_csv("../neat_data/raw_data/greened_lots.csv")
greened_clean_df = greened_lots_df
greened_clean_df['date_season_begin'] = pd.to_datetime(greened_clean_df['date_season_begin'])
greened_clean_df = greened_clean_df.dropna(subset=['date_season_begin'])

# Change fall dates to be more accurate
greened_clean_df['date_season_begin'] = greened_clean_df.apply(
        lambda x: x.date_season_begin + relativedelta(months=+6) \
        if x.season == "Fall" else x.date_season_begin, axis=1)

greened_clean_df = greened_clean_df[['id', 'date_season_begin', 'lon', 'lat']]

greened_clean_df = greened_clean_df[(greened_clean_df.date_season_begin <= datetime(2018, 6, 30)) &
                                    (greened_clean_df.date_season_begin >= datetime(2007, 7, 1))]

greened_clean_df.to_csv("../neat_data/cleaned_data/cleaned_greened_lots.csv")

# Clean the vacant lots data
# Only include lots that were marked as vacant between 9/01/2007 - 09/01/2017
# Same range as greened lots
viol_df = pd.read_csv("../neat_data/raw_data/li_violations.csv")

# Subset on just vacant violations
clean_vac_df = viol_df[viol_df['violationdescription'].str.contains("VACANT LOT") == True]

clean_vac_df['violationdate'] = pd.to_datetime(clean_vac_df['violationdate'])

clean_vac_df = clean_vac_df.dropna(subset=['violationdate','lng', 'lat'])

clean_vac_df = clean_vac_df[(clean_vac_df.violationdate <= datetime(2017, 9, 1)) &
                            (clean_vac_df.violationdate >= datetime(2007, 9, 1))]

clean_vac_df = clean_vac_df.sort_values(by=['violationdate'])
clean_vac_df = clean_vac_df.drop_duplicates(subset=['address'], keep='first')

clean_vac_df = clean_vac_df[['objectid', 'violationdate', 'lng', 'lat']]

# Now ensure that no vacant lot is within any greened lot (100m radius)

# Define a function to create a circlea around a coordinate

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

# First create a megaobject that is the union of greened lots using 50m radius
all_green_lots = []

for index, row in greened_clean_df.iterrows():
    all_green_lots.append(Polygon(geodesic_point_buffer(row.lat, row.lon, 0.05)))
    
greened_lots_areas = cascaded_union(all_green_lots)

# Now find all the indices of the vacant lots that aren't within the greened lots
good_indices = []

count = 0
for index, row in clean_vac_df.iterrows():
    count += 1
    if (count % 100) == 0:
        print("Lot count: ", count)
    curr_coord = Point(row.lng, row.lat)
    
    if not greened_lots_areas.contains(curr_coord):
        good_indices.append(index)
    
clean_vac_df_no_green = clean_vac_df.loc[good_indices]

clean_vac_df_no_green.to_csv("../neat_data/cleaned_data/cleaned_vacant_lots.csv")

# Clean the crime data
# Also only include crimes that are relevant

crime_df_all = pd.read_csv("../neat_data/raw_data/crime.csv")

crime_df = crime_df_all[['dispatch_date', 'lat', 'lng', 'ucr_general', 'text_general_code']]

# Drop all rows with NANs
crime_df = crime_df.dropna()

# Drop all crimes that aren't relevant
relevant_codes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1400, 2000, 2300, 2400, 2500]
crime_df = crime_df[crime_df['ucr_general'].isin(relevant_codes)]

# Drop the recovered stolen vehicles section
crime_df = crime_df[crime_df['text_general_code'] != "Recovered Stolen Motor Vehicle"]

# Make sure crime data has date time settings for its date
crime_df['dispatch_date'] = pd.to_datetime(crime_df['dispatch_date'])

# Subset crime data to be between the range of date plus and minus 18 months
upper_limit = datetime(2017, 9, 1) + relativedelta(months=+18)
lower_limit = datetime(2007, 9, 1) - relativedelta(months=+18)

crime_df = crime_df[(crime_df.dispatch_date >= lower_limit) & (crime_df.dispatch_date <= upper_limit)]

crime_df.to_csv("../neat_data/cleaned_data/cleaned_crimes.csv")


