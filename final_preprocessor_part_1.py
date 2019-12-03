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

print("STEP 1: Process lots data")
greened_lots_prop_df = pd.read_csv("data/raw_data/greened_lots.csv")
greened_lots_prop_df = greened_lots_prop_df[['id', 'date_season_begin']]

zone_file_list = ['Civ0', 'Com1', 'Cul2', 'Ind3', 'Oth4', 'Tra6', 'Vac7', 'Wat8']
zone_name_list = ['Civic', 'Commercial', 'Cultural', 'Industrial', 'Other', 'Transportation', 'Vacant', 'Water']

radius_area = 1.32216174888427e-05

for i in range(8):
    file_name = 'data/processed_data/Land_Use/Lot_Proportions_Final/greened_areas_' + zone_file_list[i] + '.pickle'
    with open(file_name, 'rb') as handle:
        areas_list = pickle.load(handle)
    propor_list = [x / radius_area for x in areas_list]
    
    greened_lots_prop_df[zone_name_list[i]] = propor_list
    
# Add residential in there
greened_lots_prop_df['Residential'] = greened_lots_prop_df.apply(lambda row: 1 - row[3:].sum(), axis = 1)
    
print("Step 2: Join together")
# Retrieve the demographic and economic data too and join that to main dataset
greened_lots_demo_econ_df = pd.read_csv("data/processed_data/greened_lots_demo_econ.csv")
greened_lots_demo_econ_df = greened_lots_demo_econ_df.drop(columns=['Unnamed: 0', 'census_block_index', 'Margin of Error; Per capita income in the past 12 months (in 2015 Inflation-adjusted dollars)'])
greened_lots_demo_econ_df.iloc[:,2:-1] = greened_lots_demo_econ_df.iloc[:,2:-1].div(greened_lots_demo_econ_df['Total:'], axis=0)

greened_lots_total_df = greened_lots_prop_df.set_index('id').join(greened_lots_demo_econ_df.set_index('lot_id'))

# Save the file
greened_lots_total_df.to_csv("data/processed_data/greened_lots_attributes.csv")