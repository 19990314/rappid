This is the README file for the RAPPIT project

run_laplacian.sh:
the mission control center distributing tasks:
Step 0: Assigning global variables
Step 1: Activating Conda Env and log file
Step 2: Check subjects and file existence
Step 3: Generate Meta file
Step 4: Prepare time book and log file
Step 5: Run Laplacian

single_laplacian.sh:
the bash script initiating laplacian calculation for individual subject
it is the script that qsub calls to post tasks

laplacian_caller.py:
processing all the info we need: mask files for white, grey matter, and the PAS segmentation
then calling laplacian_calculator to do the calculation

laplacian_calculator.py:
calculate the laplacian potentials

meta_info_generator.py:
generate the meta file (meta_info_per_sub.csv) with input file information for each subject

visualization.py:
construct laplacian field into 3D visualization