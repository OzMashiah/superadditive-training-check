import pandas as pd
import os
import matplotlib.pyplot as plt
#import seaborn as sns
#import statsmodels.api as sm
import scipy
#import scikit_posthocs as sp
import re
import glob
import numpy as np
import params

# Functions to categorise trials data to simpler columns.
def categorise_correct(row):  
    '''This function gets a row and returns yes if the subject was correct with his answer and no if he was incorrect'''
    if (row['angleChange'] != 0 or row['SensoMotoric Delay'] != 0) and row['QuestionResult'] == 0 :
        return 'yes'
    elif row['angleChange'] == 0 and row['SensoMotoric Delay'] == 0 and row['QuestionResult'] == 1 :
        return 'yes'
    return 'no'

def categorise_spatial_alteration_level(row, alteration_levels):  
    '''This function gets a row and a list of alteration levels and returns the level of spatial alteration,
    1 signifies no alteration''' 
    alteration_levels.sort()
    if row['angleChange'] == 0 :
        return '1'
    elif row['angleChange'] == alteration_levels[0] or row['angleChange'] == -1 * alteration_levels[0]:
        return '2'
    elif row['angleChange'] == alteration_levels[1] or row['angleChange'] == -1 * alteration_levels[1]:
        return '3'
    elif row['angleChange'] == alteration_levels[2] or row['angleChange'] == -1 * alteration_levels[2]:
        return '4'
    
def categorise_temporal_alteration_level(row, alteration_levels):  
    '''This function gets a row and a list of alteration levels and returns the level of temporal alteration,
    1 signifies no alteration''' 
    alteration_levels.sort()
    if row['SensoMotoric Delay'] == 0 :
        return '1'
    elif row['SensoMotoric Delay'] == alteration_levels[0]:
        return '2'
    elif row['SensoMotoric Delay'] == alteration_levels[1]:
        return '3'
    elif row['SensoMotoric Delay'] == alteration_levels[2]:
        return '4'

# merge results and trials files.
results = pd.read_csv(glob.glob(params.training_results_path)[0])
trials = pd.read_csv(glob.glob(params.training_trials_path)[0])
trials.drop(trials.tail(1).index, inplace = True)
trials.rename(columns = {'#trial number':'TrialNumber'}, inplace = True)
merged = pd.merge(results, trials, on='TrialNumber')

# create the preprocessed dir if doesnt exist, empties if it does exist.
if not os.path.exists(params.preprocessed_output_dir):
        os.makedirs(params.preprocessed_output_dir)
else:
    for file in os.listdir(params.preprocessed_output_dir):
        os.remove(params.preprocessed_output_dir + "/" + file)
        
merged_clean = merged[['TrialNumber', 'block number', 'SensoMotoric Delay', 'angleChange','setup task Number', 'QuestionResult']]
merged_clean.to_csv(params.preprocessed_output_dir + "/preprocessed_training.csv", index = False)
    
# Calculate the simpler necessary columns using the categorise functions in order to continue with further analysis.
data = pd.read_csv(params.preprocessed_output_dir +  "/preprocessed_training.csv")
data.drop(data.loc[data['setup task Number']==66].index, inplace=True)
data['correct'] = data.apply(lambda row: categorise_correct(row), axis=1)
data['temporalAlterationLevel'] = data.apply(lambda row: 
                                            categorise_temporal_alteration_level(row, params.temporal_alteration_levels), axis=1)
data['spatialAlterationLevel'] = data.apply(lambda row: 
                                            categorise_spatial_alteration_level(row, params.spatial_alteration_levels), axis=1)
data.to_csv(params.preprocessed_output_dir + "/categorised_training.csv", index=False)
    
    
    
    
    
# create output dir with jpgs and subject ids, training type, date.
# choose between self-attribution or correct % to display.