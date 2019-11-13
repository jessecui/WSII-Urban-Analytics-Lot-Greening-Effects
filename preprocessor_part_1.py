#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preprocesses basic data from crime and lots datasets and clean them

@author: jessecui
"""

import pandas as pd
import json

# Read in CSV and GeoJSON of Philly Crime data
crime_df = pd.read_csv("data/crime.csv")

crime_df_head = crime_df.head()

crime_df['dispatch_date'].sort_values()

# Read in vacant violations and only use vacant lots
viol_df = pd.read_csv("data/li_violations.csv")

viol_df = viol_df[viol_df['violationdescription'].str.contains("VACANT LOT") == True]

viol_df['violationdescription'].unique()

viol_df = viol_df.sort_values(by=['violationdate'])
viol_df = viol_df.drop_duplicates(subset=['address'], keep='first')
viol_df.to_csv("data/vacant_lots.csv")

# Read and analyze Greened Lots Data
greened_df = pd.read_csv('data/greened_lots.csv')
greened_df_head = greened_df.head()