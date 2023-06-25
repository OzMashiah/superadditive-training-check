# superadditive-training-check
A script for checking the subject's training performance to decide if there is a need for repeating or if we can continue.

The params file got all the basic paths and alteration levels. (if anything changed since 25.06.2023 make sure to change there too)

The necessary things to run are the Python main script, the params file, and a /Data (which can be changed via the params file) 
directory in the same folder containing only **one** folder of a training run. The folder is the same folder we can as an output from the Alice
program, for example: "Sub-157_Plan-Training_UI_RunID-20230618-160519". No need to change anything just drop it in the data directory.

The necessary Python modules for this program are: pandas, os, matplotlib, glob, and sys. All can be downloaded via pip install if needed.

To run the program just run the training-check.py file using Python.

The results will be outputted to the results_output_dir parameter (default to /Results).


