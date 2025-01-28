#
# RAPPIT
A Region-Specific MRI Metric for Assessing Glymphatic Function. We aim to reconstruct the fluid kenetics (the diffusive trajectories of water molecules) between periarterial spaces (PAS) and parenchyma area.

  

## Conda Env

It has been packed into laplacian.yml  
You can set it up using: 
***conda env create -f laplacian.yml***  
  

## Pipeline execution order

***1. run_laplacian.sh -> [meta_info_generator.py, single_laplacian.sh]  
2. single_laplacian.sh -> laplacian_caller.py -> laplacian_calculator.py  
3. visualization.py***  


## Scripts
***run_laplacian.sh:***  
the mission control center distributing tasks:  
Step 0: Assigning global variables  
Step 1: Activating Conda Env and log file  
Step 2: Check subjects and file existence  
Step 3: Generate Meta file  
Step 4: Prepare time book and log file  
Step 5: Run Laplacian  
  
***single_laplacian.sh:***  
the bash script initiating laplacian calculation for individual subject  
it is the script that qsub calls to post tasks  
  
***laplacian_caller.py:***  
processing all the info we need: mask files for white, grey matter, and the PAS segmentation  
then calling laplacian_calculator to do the calculation  
  
***laplacian_calculator.py:***  
calculate the laplacian potentials  
  
***meta_info_generator.py:***  
generate the meta file (meta_info_per_sub.csv) with input file information for each subject  
  
***visualization.py:***  
construct laplacian field into 3D visualization


## Notice
**Rappid**

We are still working on this project. Please feel free to contact us if you are interested in it. Also, if you use or build upon the methods, data, or findings presented in this project, please provide appropriate attribution of it.
Proper citation helps acknowledge the contributions of this work and supports further research in this area. 

Copyright [2025] [NIDLL lab, University of Southern California]

