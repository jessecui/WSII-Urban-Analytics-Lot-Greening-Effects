#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 23:27:52 2019

@author: jessecui

Preprocess the greened lots dataset to one final dataset
"""

import pandas as pd
import pickle
from ast import literal_eval

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
greened_with_crime_df['violent_200_before'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_before'])), axis = 1)
greened_with_crime_df['violent_200_after'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['100_after'])), axis = 1)
greened_with_crime_df['nonviolent_200_before'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_before'])), axis = 1)
greened_with_crime_df['nonviolent_200_after'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['100_after'])), axis = 1) 

print("STEP 2c: Count crimes 500 meter radius")
greened_with_crime_df['violent_500_before'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_before'])), axis = 1)
greened_with_crime_df['violent_500_after'] = greened_with_crime_df.apply(lambda row: sum(i <= 400 for i in literal_eval(row['500_after'])), axis = 1)
greened_with_crime_df['nonviolent_500_before'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_before'])), axis = 1)
greened_with_crime_df['nonviolent_500_after'] = greened_with_crime_df.apply(lambda row: sum(i > 400 for i in literal_eval(row['500_after'])), axis = 1) 

greened_with_crime_df = greened_with_crime_df.drop(columns=['100_before', '100_after', '200_before', '200_after', '500_before', '500_after'])

# Drop years 2006 and 2019
greened_with_crime_df = greened_with_crime_df[(greened_with_crime_df['year'] != 2006) & (greened_with_crime_df['year'] != 2019)]

print("STEP 3: Append lots data")
greened_lots_prop_df = pd.read_csv("data/raw_data/greened_lots.csv")
greened_lots_prop_df = greened_lots_prop_df[['id']]

zone_file_list = ['Civ0', 'Com1', 'Cul2', 'Ind3', 'Oth4', 'Tra6', 'Vac7', 'Wat8']
zone_name_list = ['Civic', 'Commercial', 'Cultural', 'Industrial', 'Other', 'Transportation', 'Vacant', 'Water']

radius_area = 1.32216174888427e-05

for i in range(8):
    file_name = 'data/processed_data/Land_Use/Lot_Proportions_Final/greened_areas_' + zone_file_list[i] + '.pickle'
    with open(file_name, 'rb') as handle:
        areas_list = pickle.load(handle)
    propor_list = [x / radius_area for x in areas_list]
    
    greened_lots_prop_df[zone_name_list[i]] = propor_list
    
print("Step 4: Join on Index")
greened_lots_total_df = greened_with_crime_df.set_index('id').join(greened_lots_prop_df.set_index('id'))

# Retrieve the demographic and economic data too and join that to main dataset
greened_lots_demo_econ_df = pd.read_csv("data/processed_data/greened_lots_demo_econ.csv").set_index('lot_id')
greened_lots_demo_econ_df = greened_lots_demo_econ_df.drop(columns=['Unnamed: 0', 'census_block_index', 'Margin of Error; Per capita income in the past 12 months (in 2015 Inflation-adjusted dollars)'])
greened_lots_demo_econ_df.iloc[:,1:-2] = greened_lots_demo_econ_df.iloc[:,1:-2].div(greened_lots_demo_econ_df['Total:'], axis=0)

greened_lots_total_df = greened_lots_total_df.join(greened_lots_demo_econ_df)

# Save the file
greened_lots_total_df.to_csv("data/processed_data/greened_lots_final.csv")






