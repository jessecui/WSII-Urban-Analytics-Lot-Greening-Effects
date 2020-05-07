#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takes the output of crime parsers (the files beginning with 
4_get_crimes_per.....lot.py) and counts up the total violent and
non-violent crimes for each lot.

@author: jessecui
"""

import pandas as pd
from ast import literal_eval
import datetime

print("STEP 1: Process the crime appended data")
greened_with_crime_df = pd.read_csv("../neat_data/processed_data/greened_lots_crimes.csv")
greened_with_crime_df = greened_with_crime_df[['id', 'date_season_begin', '100_before', '100_after', '200_before', '200_after', '500_before', '500_after']]

greened_with_crime_final_df = greened_with_crime_df.copy()

# Count the number of violent and non-violent crimes before and after
print("STEP 2a: Count crimes 100 meter radius")
greened_with_crime_final_df['violent_100_before'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_before'])), axis = 1)
greened_with_crime_final_df['violent_100_after'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_after'])), axis = 1)
greened_with_crime_final_df['nonviolent_100_before'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_before'])), axis = 1)
greened_with_crime_final_df['nonviolent_100_after'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_after'])), axis = 1) 

print("STEP 2b: Count crimes 200 meter radius")
greened_with_crime_final_df['violent_200_before'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['200_before'])), axis = 1)
greened_with_crime_final_df['violent_200_after'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['200_after'])), axis = 1)
greened_with_crime_final_df['nonviolent_200_before'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['200_before'])), axis = 1)
greened_with_crime_final_df['nonviolent_200_after'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['200_after'])), axis = 1) 

print("STEP 2c: Count crimes 500 meter radius")
greened_with_crime_final_df['violent_500_before'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_before'])), axis = 1)
greened_with_crime_final_df['violent_500_after'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_after'])), axis = 1)
greened_with_crime_final_df['nonviolent_500_before'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_before'])), axis = 1)
greened_with_crime_final_df['nonviolent_500_after'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_after'])), axis = 1) 

greened_with_crime_final_df = greened_with_crime_final_df.drop(columns=['100_before', '100_after', '200_before', '200_after', '500_before', '500_after'])

greened_with_crime_final_df.to_csv("../neat_data/processed_data/greened_lots_crime_counts.csv")


# --------------------------------------
# VACANT LOTS WITH MATCHING
vacant_crime_df = pd.read_csv("../neat_data/processed_data/vacant_lots_crimes_new.csv")
vacant_crime_df = vacant_crime_df[['vacant_id', 'greened_id', 'match_greened_date', '100_before', '100_after', '200_before', '200_after', '500_before', '500_after']]
vacant_crime_final_df = vacant_crime_df.copy()

# Count the number of violent and non-violent crimes before and after
print("STEP 2a: Count crimes 100 meter radius")
vacant_crime_final_df['violent_100_before'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_before'])), axis = 1)
vacant_crime_final_df['violent_100_after'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_after'])), axis = 1)
vacant_crime_final_df['nonviolent_100_before'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_before'])), axis = 1)
vacant_crime_final_df['nonviolent_100_after'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_after'])), axis = 1) 

print("STEP 2b: Count crimes 200 meter radius")
vacant_crime_final_df['violent_200_before'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['200_before'])), axis = 1)
vacant_crime_final_df['violent_200_after'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['200_after'])), axis = 1)
vacant_crime_final_df['nonviolent_200_before'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['200_before'])), axis = 1)
vacant_crime_final_df['nonviolent_200_after'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['200_after'])), axis = 1) 

print("STEP 2c: Count crimes 500 meter radius")
vacant_crime_final_df['violent_500_before'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_before'])), axis = 1)
vacant_crime_final_df['violent_500_after'] = vacant_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_after'])), axis = 1)
vacant_crime_final_df['nonviolent_500_before'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_before'])), axis = 1)
vacant_crime_final_df['nonviolent_500_after'] = vacant_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_after'])), axis = 1) 

vacant_crime_final_df = vacant_crime_final_df.drop(columns=['100_before', '100_after', '200_before', '200_after', '500_before', '500_after'])

vacant_crime_final_df.to_csv("../neat_data/processed_data/vacant_lots_crime_counts_new.csv")