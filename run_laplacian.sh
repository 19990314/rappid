#!/bin/sh
#PBS -o job_output.log
source ~/../shuchen/miniconda3/bin/activate
conda activate laplacian

proj_root=/ifs/loni/faculty/hkim/shuting/code/
output_file_path=${proj_root}/output_from_pipeline/
subject_file_path=/ifs/loni/faculty/hkim/hedong/DTI_NODDI/listfile/HCA_625ascend.txt
wm_dir=/ifs/loni/faculty/hkim/yaqiong/HCP-A-CIVET2/
outsidedir=/ifs/loni/faculty/hkim/yaqiong/HCP-A-CIVET2/
pas_dir=/ifs/loni/faculty/hkim/hedong/HCP_A_PVS_label/prediction_label/PVS_instance_3_396/

echo "============************ Step 1: Check subjects and file existence ****************========="
#python3 ${proj_root}code/meta_info_generator.py --check_file_paths

echo "=============************ Step 2: Generate Meta file ****************=================="
#python3 ${proj_root}code/meta_info_generator.py

echo "=============************* Step 3: Run Laplacian *******************================"
echo "subject_id,time_used,status" > ${output_file_path}time_book.csv
for x in `cat ${subject_file_path}`
do
qsub -q compute7.q -j y -o ${output_file_path}log_laplacian -N ${x} ${proj_root}code/single_laplacian.sh ${sample} ${proj_root} ${output_file_path}
done