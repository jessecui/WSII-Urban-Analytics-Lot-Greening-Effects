#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 22:00:57 2019

@author: jessecui

Preprocess the vacant lots dataset to one final dataset
"""

import pandas as pd
import pickle
from ast import literal_eval

print("STEP 1: Process lots data")
vacant_lots_prop_df = pd.read_csv("data/raw_data/vacant_lots.csv")
vacant_lots_prop_df = vacant_lots_prop_df[['objectid', 'violationdate']]

zone_file_list = ['Civ0', 'Com1', 'Cul2', 'Ind3', 'Oth4', 'Tra6', 'Vac7', 'Wat8']
zone_name_list = ['Civic', 'Commercial', 'Cultural', 'Industrial', 'Other', 'Transportation', 'Vacant', 'Water']

radius_area = 1.32216174888427e-05

for i in range(8):
    file_name = 'data/processed_data/Land_Use/Lot_Proportions_Final/vacant_areas_' + zone_file_list[i] + '.pickle'
    with open(file_name, 'rb') as handle:
        areas_list = pickle.load(handle)
    propor_list = [x / radius_area for x in areas_list]
    
    vacant_lots_prop_df[zone_name_list[i]] = propor_list
    
# Add residential in there
vacant_lots_prop_df['Residential'] = vacant_lots_prop_df.apply(lambda row: 1 - row[3:].sum(), axis = 1)
    
print("Step 2: Join together")
# Retrieve the demographic and economic data too and join that to main dataset
vacant_lots_demo_econ_df = pd.read_csv("data/processed_data/vacant_lots_demo_econ.csv")
vacant_lots_demo_econ_df = vacant_lots_demo_econ_df.drop(columns=['Unnamed: 0', 'census_block_index', 'Margin of Error; Per capita income in the past 12 months (in 2015 Inflation-adjusted dollars)'])
vacant_lots_demo_econ_df.iloc[:,2:-1] = vacant_lots_demo_econ_df.iloc[:,2:-1].div(vacant_lots_demo_econ_df['Total:'], axis=0)

vacant_lots_total_df = vacant_lots_prop_df.set_index('objectid').join(vacant_lots_demo_econ_df.set_index('lot_id'))

# Save the file
vacant_lots_total_df.to_csv("data/processed_data/vacant_lots_attributes.csv")