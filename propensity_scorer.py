#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 03:09:24 2019

@author: jessecui
"""

import pandas as pd
from sklearn.linear_model import LinearRegression

greened_lots_df = pd.read_csv("data/processed_data/greened_lots_attributes.csv").drop(columns=['date_season_begin']).set_index('id').dropna()
vacant_lots_df = pd.read_csv("data/processed_data/vacant_lots_attributes.csv").drop(columns=['violationdate']).set_index('objectid').dropna()

greened_lots_df['is_greened'] = 1
vacant_lots_df['is_greened'] = 0

total_df = greened_lots_df.append(vacant_lots_df)

X = total_df.iloc[:, :-1]
y = total_df.iloc[:, -1]

clf = LinearRegression().fit(X,y)
propensity_scores = clf.predict(X)

greened_lots_df['propensity'] = propensity_scores[:greened_lots_df.shape[0]]
vacant_lots_df['propensity'] = propensity_scores[greened_lots_df.shape[0]:]