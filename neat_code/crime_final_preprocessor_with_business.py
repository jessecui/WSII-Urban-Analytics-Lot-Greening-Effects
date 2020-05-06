#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:34:16 2020

@author: jessecui
"""

import pandas as pd
from ast import literal_eval
import datetime

# --------------------------------------
# VACANT LOTS WITH MATCHING
vacant_crime_df = pd.read_csv("../neat_data/processed_data/vacant_lots_crimes_with_business_new.csv")
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

vacant_crime_final_df.to_csv("../neat_data/processed_data/vacant_lots_crime_counts_with_business_new.csv")