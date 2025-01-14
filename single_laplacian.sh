#!/bin/sh
source ~/../shuchen/miniconda3/bin/activate
conda activate laplacian
echo "Conda Env has been activated"

sample=$1
proj_root=$2
output_file_path=$3
echo "processing sample......"
#echo "calling ${proj_root}code/laplacian_caller.py"
python3 ${proj_root}code/laplacian_caller.py --sample ${sample} --output_dir ${output_file_path}