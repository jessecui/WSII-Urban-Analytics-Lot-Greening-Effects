#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 23:05:10 2019

@author: jessecui
"""
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