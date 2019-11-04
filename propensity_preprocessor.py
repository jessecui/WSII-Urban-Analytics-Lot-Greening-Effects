#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 18:23:03 2019

Creates a data matrix with demographic and economic data per lot

@author: jessecui
"""

import pandas as pd
import geopandas as gpd

# Pull the raw demographic and economic data per block
demographic_df = pd.read_csv("data/raw_data/demographic_data.csv", header=1)
economic_df = pd.read_csv("data/raw_data/economic_data.csv", header=1)

# Drop the columns that will be duplicated between the two tables
demographic_df = demographic_df.drop(['Id', 'Geography'], axis=1)

# Merge the two tables
demo_econ_df = economic_df.merge(demographic_df, left_on='Id2', right_on='Id2')

# Drop unnecessary columns and force the entries to be numeric
demo_econ_df = demo_econ_df.drop(['Id', 'Geography'], axis=1)
demo_econ_df.iloc[:, -1] = pd.to_numeric(demo_econ_df.iloc[:, -1], errors='coerce')
demo_econ_df.iloc[:, -2] = pd.to_numeric(demo_econ_df.iloc[:, -2], errors='coerce')

# Merge this table with the greened lots df
greened_lots_df = pd.read_csv("data/processed_data/greened_lots_with_block.csv")
greened_lots_core_df = greened_lots_df[['id', 'census_block_index']]
greened_lots_demo_econ_df = greened_lots_core_df\
                                .merge(demo_econ_df, left_on='census_block_index', right_on='Id2')\
                                .drop(['Id2'], axis=1).rename(columns={'id': "lot_id"})
greened_lots_demo_econ_df.to_csv("data/processed_data/greened_lots_demo_econ.csv")
                                
vacant_lots_df = pd.read_csv("data/processed_data/vacant_lots_with_block.csv")
vacant_lots_core_df = vacant_lots_df[['objectid', 'census_block_index']]
vacant_lots_demo_econ_df = vacant_lots_core_df\
                                .merge(demo_econ_df, left_on='census_block_index', right_on='Id2')\
                                .drop(['Id2'], axis=1).rename(columns={'objectid': "lot_id"})
                                
vacant_lots_demo_econ_df.to_csv("data/processed_data/vacant_lots_demo_econ.csv")