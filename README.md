# Business Vibrancy Urban Analytics Project
This project for my work as a research fellow at the Wharton Social Impact Initiative, analyzing effects of greening lots on crime and how business vibrancy characteristics influence this affect.

## Data
The datasets are split into several folders. The datasets are in neat_data. Within this folder, there are several sub folders.

The folders contained are:
1. raw_data contains the raw data that I retrieved from OpenDataPhilly, previous work from this project, ACS, etc.
1. cleaned_data contains the cleaned and filtered crimes, vacant lots, and greened lots datasets.
1. analysis_results contains the results from t-tests.
1. processed_data contains most of the intermediate preprocessed data, such as crime counts, attributes per vacant lot. I created a folder called most_important_data to contain the most important data from this set. These data includes lots attributes, matching results with business data, and the crime counts for greened and vacant lots using the matches.


## Code
The preprocessing and analysis code are in neat_code. The code files are numbered in approximately the order it takes to run the analysis. Code sections from 1-5 is preprocessing, matching, and analyzing data without business data. Starting at the code file beginning with 6_, we use business data and preprocess, match, and analyze lots data.

Essentially, if we're only using business matches, feel free to skip pipeline numbers 3, 4, and 5 since those get repeated with pipeline numbers 7, 8, and 9 but including business data.

Code files numbered 10-14 are analysis files from the results of the crime counts. 10 and 11 are t-tests and plot generators on data without business matching, while files 12 and 13 are t-tests and plot generators with business data. File number 14 is plot generators for all data, from summary analysis on vacant and greened lot characterstics to the analysis of the propensity model.

For business vibrancy matching, the most important pipelines to look at is 1, 2 and 6 for preprocessing data, 7 for propensity scoring and matching, 4 (the greened lots one), 8, and 9 for getting crime counts, 12 for t-tests, and 11 and 13 for plotting charts. However, you'll have to change 11's file path location to use business data's t-test results since it currently uses the non-business data t-tests results.  

Note some file paths may have changed since refactoring the code so double check that the file paths for datasets link to the right file locations.

## Archived Code
There is archived code in archived_old_code under the archive_folders_2019. This is code I wrote in Fall 2019, but contains code on how to process land use proportions per lot and how to create a large attributes dataset for greened and vacant lots.
