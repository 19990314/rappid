#!/bin/sh
echo "============************ Step 0: Assigning global variables ****************========="
proj_root=/ifs/loni/faculty/hkim/shuting/code/

# section A: ADNI project
project_name=ADNI
output_file_path=${proj_root}output_from_pipeline_ADNI/
subject_file_path=/ifs/loni/faculty/hkim/hedong/DTI_NODDI/listfile/adni_114jmp.txt
wm_dir=/ifs/loni/faculty/hkim/hedong/DTI_NODDI/ADNI3/CIVET_out/
outsidedir=/ifs/loni/faculty/hkim/hedong/DTI_NODDI/ADNI3/CIVET_out/
pas_dir=/ifs/loni/faculty/hkim/hedong/DTI_NODDI/ADNI3/nnUNet_raw/ADNI_T1_pred_002_union/
meta_file_path=${proj_root}output_from_pipeline/meta_file_tracker_ADNI.csv
timebook_name=time_book_ADNI.csv

# section B: HCP project
project_name=HCP
output_file_path=${proj_root}output_from_pipeline/
subject_file_path=/ifs/loni/faculty/hkim/hedong/DTI_NODDI/listfile/HCA_625ascend.txt
wm_dir=/ifs/loni/faculty/hkim/yaqiong/HCP-A-CIVET2/
outsidedir=/ifs/loni/faculty/hkim/yaqiong/HCP-A-CIVET2/
pas_dir=/ifs/loni/faculty/hkim/hedong/HCP_A_PVS_label/prediction_label/PVS_instance_3_396/
meta_file_path=${proj_root}output_from_pipeline/meta_file_tracker2.csv
timebook_name=time_book2.csv

# just switch the section of your target project to the bottom so the variables will be overwritten

echo "============************ Step 1: Activating Conda Env and log file ****************========="
source ~/../shuchen/miniconda3/bin/activate
conda activate laplacian
echo "Conda Env has been activated"

if [ -e "${output_file_path}log_laplacian" ]; then
    echo "Log file for jobs from: $(date +"%H:%M:%S")" > "${output_file_path}log_laplacian"
fi
echo "Log file for jobs from: $(date +"%M:%D:%H:%M:%S")"


echo "============************ Step 2: Check subjects and file existence ****************========="
#python3 ${proj_root}code/meta_info_generator.py --check_file_paths --subject_input ${subject_file_path} --wm_dir ${wm_dir} --outside_dir ${outsidedir} --pas_dir ${pas_dir} --output ${meta_file_path} --project_name ${project_name}

echo "=============************ Step 3: Generate Meta file ****************=================="
#python3 ${proj_root}code/meta_info_generator.py --subject_input ${subject_file_path} --wm_dir ${wm_dir} --outside_dir ${outsidedir} --pas_dir ${pas_dir} --output ${meta_file_path} --project_name ${project_name}

echo "=============************ Step 4: Prepare time book and log file ****************=================="
if [ -e "${output_file_path}${timebook_name}" ]; then
    rm "${output_file_path}${timebook_name}"
    echo "subject_id,time_used,status" > ${output_file_path}${timebook_name}
fi
if [ -d "${output_file_path}${project_name}_log/" ]; then
    rm -rf "${output_file_path}${project_name}_log/"
fi
mkdir "${output_file_path}${project_name}_log"
if [ ! -d "${output_file_path}voxel_counts/" ]; then
    mkdir "${output_file_path}voxel_counts/"
fi

echo "=============************* Step 5: Run Laplacian *******************================"
#for x in `cat ${subject_file_path}`
for x in `cut -d',' -f1 /ifs/loni/faculty/hkim/shuting/code/output_from_pipeline/meta_file_tracker2.csv | tail -n +2`
do
#qsub -q runnow.q -j y -o ${output_file_path}log/log_${x} -N ${x} ${proj_root}code/single_laplacian.sh ${x} ${proj_root} ${output_file_path}
qsub -q runnow.q -j y -o ${output_file_path}${project_name}_log -N ${x} ${proj_root}code/single_laplacian.sh ${x} ${proj_root} ${output_file_path}  ${meta_file_path} ${timebook_name}
done