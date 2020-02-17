#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 23:05:10 2019

@author: jessecui
"""

import pandas as pd
from ast import literal_eval
import datetime

print("STEP 1: Process the crime appended data")
greened_with_crime_df = pd.read_csv("data/processed_data/processed_greened_lots_with_crimes.csv")
greened_with_crime_df = greened_with_crime_df[['id', 'year', 'date_season_begin', '100_before', '100_after', '200_before', '200_after', '500_before', '500_after']]

# Count the number of violent and non-violent crimes before and after
print("STEP 2a: Count crimes 100 meter radius")
greened_with_crime_df['violent_100_before'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_before'])), axis = 1)
greened_with_crime_df['violent_100_after'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_after'])), axis = 1)
greened_with_crime_df['nonviolent_100_before'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_before'])), axis = 1)
greened_with_crime_df['nonviolent_100_after'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_after'])), axis = 1) 

print("STEP 2b: Count crimes 200 meter radius")
greened_with_crime_df['violent_200_before'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['200_before'])), axis = 1)
greened_with_crime_df['violent_200_after'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['200_after'])), axis = 1)
greened_with_crime_df['nonviolent_200_before'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['200_before'])), axis = 1)
greened_with_crime_df['nonviolent_200_after'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['200_after'])), axis = 1) 

print("STEP 2c: Count crimes 500 meter radius")
greened_with_crime_df['violent_500_before'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_before'])), axis = 1)
greened_with_crime_df['violent_500_after'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_after'])), axis = 1)
greened_with_crime_df['nonviolent_500_before'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_before'])), axis = 1)
greened_with_crime_df['nonviolent_500_after'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_after'])), axis = 1) 

greened_with_crime_df = greened_with_crime_df.drop(columns=['100_before', '100_after', '200_before', '200_after', '500_before', '500_after'])

# Drop years 2006 and 2019
greened_with_crime_df = greened_with_crime_df[(greened_with_crime_df['year'] != 2006) & (greened_with_crime_df['year'] != 2019)]

greened_with_crime_df.to_csv("data/processed_data/greened_lots_crimes.csv")

# VACANT LOTS PREPROCESSING
print("STEP 1: Process the crime appended data")
crime_df_1 = pd.read_csv("data/processed_data/crime_vacant/processed_vacant_lots_with_crimes_1.csv")
crime_df_1 = crime_df_1[['objectid', 'violationdate', '100_before', '100_after', '200_before', '200_after', '500_before', '500_after']]
crime_df_2 = pd.read_csv("data/processed_data/crime_vacant/processed_vacant_lots_with_crimes_2.csv")
crime_df_2 = crime_df_2[['objectid', 'violationdate', '100_before', '100_after', '200_before', '200_after', '500_before', '500_after']]
crime_df_3 = pd.read_csv("data/processed_data/crime_vacant/processed_vacant_lots_with_crimes_3.csv")
crime_df_3 = crime_df_3[['objectid', 'violationdate', '100_before', '100_after', '200_before', '200_after', '500_before', '500_after']]

vacant_crime_df = pd.concat((crime_df_1, crime_df_2, crime_df_3), axis=0)

# Count the number of violent and non-violent crimes before and after
print("STEP 2a: Count crimes 100 meter radius")
vacant_crime_df['violent_100_before'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_before'])), axis = 1)
vacant_crime_df['violent_100_after'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_after'])), axis = 1)
vacant_crime_df['nonviolent_100_before'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_before'])), axis = 1)
vacant_crime_df['nonviolent_100_after'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_after'])), axis = 1) 

print("STEP 2b: Count crimes 200 meter radius")
vacant_crime_df['violent_200_before'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['200_before'])), axis = 1)
vacant_crime_df['violent_200_after'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['200_after'])), axis = 1)
vacant_crime_df['nonviolent_200_before'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['200_before'])), axis = 1)
vacant_crime_df['nonviolent_200_after'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['200_after'])), axis = 1) 

print("STEP 2c: Count crimes 500 meter radius")
vacant_crime_df['violent_500_before'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_before'])), axis = 1)
vacant_crime_df['violent_500_after'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_after'])), axis = 1)
vacant_crime_df['nonviolent_500_before'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_before'])), axis = 1)
vacant_crime_df['nonviolent_500_after'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_after'])), axis = 1) 

vacant_crime_df = vacant_crime_df.drop(columns=['100_before', '100_after', '200_before', '200_after', '500_before', '500_after'])

# Drop years 2006 and 2019
vacant_crime_df['violationdate'] = pd.to_datetime(vacant_crime_df['violationdate'])
vacant_crime_df['year'] = vacant_crime_df.apply(lambda row: row.violationdate.year, axis = 1)
vacant_crime_df = vacant_crime_df[(vacant_crime_df['year'] != 2006) & (vacant_crime_df['year'] != 2019)]

vacant_crime_df.to_csv("data/processed_data/vacant_lots_crimes_final.csv")

# --------------------------------------
# VACANT LOTS WITH MATCHING
vacant_crime_df = pd.read_csv("data/processed_data/processed_vacant_lots_with_crimes.csv")
vacant_crime_df = vacant_crime_df[['vacant_id', 'greened_id', 'match_greened_date', '100_before', '100_after', '200_before', '200_after', '500_before', '500_after']]
# Count the number of violent and non-violent crimes before and after
print("STEP 2a: Count crimes 100 meter radius")
vacant_crime_df['violent_100_before'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_before'])), axis = 1)
vacant_crime_df['violent_100_after'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_after'])), axis = 1)
vacant_crime_df['nonviolent_100_before'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_before'])), axis = 1)
vacant_crime_df['nonviolent_100_after'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_after'])), axis = 1) 

print("STEP 2b: Count crimes 200 meter radius")
vacant_crime_df['violent_200_before'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['200_before'])), axis = 1)
vacant_crime_df['violent_200_after'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['200_after'])), axis = 1)
vacant_crime_df['nonviolent_200_before'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['200_before'])), axis = 1)
vacant_crime_df['nonviolent_200_after'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['200_after'])), axis = 1) 

print("STEP 2c: Count crimes 500 meter radius")
vacant_crime_df['violent_500_before'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_before'])), axis = 1)
vacant_crime_df['violent_500_after'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_after'])), axis = 1)
vacant_crime_df['nonviolent_500_before'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_before'])), axis = 1)
vacant_crime_df['nonviolent_500_after'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_after'])), axis = 1) 

vacant_crime_df = vacant_crime_df.drop(columns=['100_before', '100_after', '200_before', '200_after', '500_before', '500_after'])

# Drop years 2006 and 2019
vacant_crime_df['violationdate'] = pd.to_datetime(vacant_crime_df['violationdate'])
vacant_crime_df['year'] = vacant_crime_df.apply(lambda row: row.violationdate.year, axis = 1)
vacant_crime_df = vacant_crime_df[(vacant_crime_df['year'] != 2006) & (vacant_crime_df['year'] != 2019)]

vacant_crime_df.to_csv("data/processed_data/vacant_lots_crimes_matched_final.csv")