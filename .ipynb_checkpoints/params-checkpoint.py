# Parameters - make sure to adjust before a new running environment/experiment!
data_dir = "data/" # Specify where is the subjects data directory 
trials_file_pattern = r'Trials_UI_train*' # Specify the pattern of the naming for the trials files, used as regular expression.
preprocessed_output_dir = 'Preprocessed/' # The folder where you want the preprocessed csvs to be.
results_output_dir = 'Results/' # The folder where you want the final scores to be.
spatial_alteration_levels = [0.1583, 0.2125, 0.2679] # Specify the levels of spatial alteration, only positive of each level.
temporal_alteration_levels = [0.05, 0.072, 0.094] # Specify the levels of temporal alteration.

training_results_path = data_dir  + "Sub-*_Plan*" + "/Answers*.csv"
training_trials_path = data_dir  + "Sub-*_Plan*" + "/UsedPlan/" + trials_file_pattern