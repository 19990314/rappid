#!/bin/sh
sample=${1}
proj_root=${2}
output_file_path=${3}
python3 ${proj_root}code/laplacian_caller.py --sample ${sample} --output_dir ${output_file_path}