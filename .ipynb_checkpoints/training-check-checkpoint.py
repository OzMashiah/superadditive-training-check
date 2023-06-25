import pandas as pd
from pandas.plotting import table 
import os
import matplotlib.pyplot as plt
import glob
import params
import sys

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

# make sure the data_dir exists and has only one folder in it.
if not os.path.exists(params.data_dir):
    sys.exit("The " + params.data_dir + " folder does not exists")
else:
    if not len(os.listdir(params.data_dir)) == 1:
        sys.exit("There is more or less than one file in the " + params.data_dir + " folder")

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

# Empty dataframe to save calculations.
scores = pd.DataFrame(columns=['TrainingType', 'L1', 'L2', 'L3', 'L4'])

row = [] # Initialize the trainings row
categorised_data = pd.read_csv(params.preprocessed_output_dir + "/categorised_training.csv")
if len(set(categorised_data.angleChange.tolist()))==1:
    # 1 level of angelchange means temporal training
    trainingtype = "Temporal"
    row.append(trainingtype) # TrainingType
    # L1, L2, L3, L4
    for level in range(1, len(set(categorised_data['temporalAlterationLevel'].tolist())) + 1):
        row.append(round((len(categorised_data.loc[(categorised_data['temporalAlterationLevel'] == level) &
                                         (categorised_data['correct'] == 'yes')])/
                          len(categorised_data.loc[(categorised_data['temporalAlterationLevel'] == level)]) * 100), 3))
else:
    # more than 1 level of angelchange means spatial training
    trainingtype = "Spatial"
    row.append(trainingtype) # TrainingType
    # L1, L2, L3, L4
    for level in range(1, len(set(categorised_data['spatialAlterationLevel'].tolist())) + 1):
        row.append(round((len(categorised_data.loc[(categorised_data['spatialAlterationLevel'] == level) &
                                         (categorised_data['correct'] == 'yes')])/
                          len(categorised_data.loc[(categorised_data['spatialAlterationLevel'] == level)]) * 100), 3))
scores.loc[len(scores)] = row
subject_num = os.listdir(params.data_dir)[0].split('_Plan')[0] # subject number
date_n_time = os.listdir(params.data_dir)[0].split('RunID-')[1] # date and time

# create results output dir if doesnt exist
if not os.path.exists(params.results_output_dir):
        os.makedirs(params.results_output_dir)

# Option to export as csv.        
#scores.to_csv(params.results_output_dir + "/" + subject_num + "_" + trainingtype + "_" + date_n_time + ".csv", index=False)

# Export scores as a png (default)
ax = plt.subplot(111, frame_on=False) # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis
ax.set_title(subject_num + " " + trainingtype + " Training (correct percentage)")
table(ax, scores.filter(regex=("L\d+$")),
     loc = "center")  

plt.savefig(params.results_output_dir + "/" + subject_num + "_" + trainingtype + "_" + date_n_time + ".png")