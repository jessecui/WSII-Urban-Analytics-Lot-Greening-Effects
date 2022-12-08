# Effects of Lot Greening - WSII Urban Analytics Project
This repo analyzes the effects of greening lots on crime and how business and land zone attributes surrounding lots influence this effect using matched pairs testing from propensity scoring. The data and code described here is for a paper published to EPB: Urban Analytics and City Science.

Paper: https://journals.sagepub.com/doi/abs/10.1177/23998083211050647

## Data
The data here is preprocessed from the sources listed from the paper. Specifically, this folder contains data for the violent and other crime counts per lot as well as the characteristics of each lot. There is a folder created during the pipeline called `matches/`, which contains data on paired matches from propensity scoring.

## Scripts
The scripts folder contains R scripts that process/create the data mentioned above. The first script is the propensity scorer and matching script, which matches lots based on propensity to be greened using lot attributes data, and then assigns matches for greened and ungreened lots. The second script contains the statistical tests to gather the results, and the third scripts analyzes the attributes data and results and creates visualizations from them.

## Analysis Results
This folder contains files and images from the results created by the scripts above. The images folder contains images on attributes data and effects on crime. The scoring folder contains data and metrics on the scoring model. The summary folder contains summary statistics on the lots and crimes. The tests folder contains the results of the t-tests ran on the paired matches.

## Corrections.Effects.of.Vacant.Lot.Greening.html
A subset of the distance calculations were incorrectly made in the code. This document provides a description of the bug and includes the updated tables and figures using the correct calculations.
