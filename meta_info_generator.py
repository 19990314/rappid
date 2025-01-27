#subject_id,
#pas_mask_file_path,
#white_matter_mask_file_path,
#grey_matter_mask_file_path,


import argparse
import csv
import time
import os


# Define the command-line argument parser
parser = argparse.ArgumentParser(description="Generate a CSV file with subject information.")
parser.add_argument(
    "--project_name",
    default="HCP",
    help="project name of our subjects."
)
parser.add_argument(
    "--output",
    default="/ifs/loni/faculty/hkim/shuting/code/output_from_pipeline/meta_file_tracker2.csv",
    help="Path to save the output CSV file. Default is 'output.csv'."
)
parser.add_argument(
    "--subject_input",
    default="/ifs/loni/faculty/hkim/hedong/DTI_NODDI/listfile/HCA_625ascend.txt",
    help="Path to save the subject file.."
)
parser.add_argument(
    "--wm_dir",
    default="/ifs/loni/faculty/hkim/yaqiong/HCP-A-CIVET2/",
    help="Path to save the wm file.."
)
parser.add_argument(
    "--outside_dir",
    default="/ifs/loni/faculty/hkim/yaqiong/HCP-A-CIVET2/",
    help="Path to save the outside file.."
)
parser.add_argument(
    "--pas_dir",
    default="/ifs/loni/faculty/hkim/hedong/HCP_A_PVS_label/prediction_label/PVS_instance_3_396/",
    help="Path to save the pas file.."
)
parser.add_argument(
    "--check_file_paths",
    action='store_true',
    help="Flag to check files"
)
def filename_distributer(subject_id, wm_dir, outside_dir, pas_dir, project_name):
    if project_name == "HCP":
        file1 = os.path.join(outside_dir, f"{subject_id}_V1_MR/{subject_id}_outside3_final.nii.gz")
        file2 = os.path.join(wm_dir, f"{subject_id}_V1_MR/{subject_id}_wm_2.nii.gz")
        file3a = os.path.join(pas_dir, f"PVS_{subject_id}_instances.nii.gz")
        file3b = os.path.join(pas_dir, f"PVS_{subject_id}_ref_labels_instances.nii.gz")
    elif project_name == "ADNI":
        file1 = os.path.join(outside_dir, f"{subject_id}/{subject_id}_outside3_final.nii.gz")
        file2 = os.path.join(wm_dir, f"{subject_id}/{subject_id}_wm_2.nii.gz")
        file3a = os.path.join(pas_dir, f"normalized_{subject_id}__instances.nii.gz")
        file3b = os.path.join(pas_dir, f"normalized_{subject_id}__instances.nii.gz")

    return file1, file2, file3a, file3b


def check_files(subject_ids, wm_dir, outside_dir, pas_dir, project_name):
    errors = []

    # Loop through each subject ID
    for subject_id in subject_ids:
        # Define the expected file paths
        file1, file2, file3a, file3b = filename_distributer(subject_id, wm_dir, outside_dir, pas_dir, project_name)

        # Check existence of the files
        missing_files = []
        if not os.path.exists(file1):
            missing_files.append(file1)
        if not os.path.exists(file2):
            missing_files.append(file2)
        if not (os.path.exists(file3a) or os.path.exists(file3b)):
            missing_files.append(f"{file3a} or {file3b}")

        # Record errors if any file is missing
        if missing_files:
            errors.append(f"Subject ID {subject_id} is missing: {', '.join(missing_files)}")

    # Print the results
    if errors:
        print("Errors found:")
        for error in errors:
            print(error)
    else:
        print("All files are present.")

# ============ main code starts ============
print("Reading inputs...")
# Parse the command-line arguments
args = parser.parse_args()
targets=[]
#targets=['HCA6018857', 'HCA6030645', 'HCA6053758', 'HCA6086470', 'HCA6110138', 'HCA6119257', 'HCA6139970', 'HCA6144862', 'HCA6162662', 'HCA6197580', 'HCA6198582', 'HCA6234964', 'HCA6253867', 'HCA6291976', 'HCA6295782', 'HCA6312352', 'HCA6320048', 'HCA6326767', 'HCA6333158', 'HCA6337974', 'HCA6374576', 'HCA6375275', 'HCA6388082', 'HCA6451366', 'HCA6464678', 'HCA6465175', 'HCA6471675', 'HCA6531667', 'HCA6574685', 'HCA6595188', 'HCA6606571', 'HCA6633069', 'HCA6660880', 'HCA6670479', 'HCA6680987', 'HCA6706373', 'HCA6742377', 'HCA6750477', 'HCA6766290', 'HCA6773691', 'HCA6787399', 'HCA6867296', 'HCA6877300', 'HCA6909286', 'HCA6910372', 'HCA6924080', 'HCA6943690', 'HCA6947294', 'HCA6987206', 'HCA7011040', 'HCA7046968', 'HCA7066873', 'HCA7075369', 'HCA7079074', 'HCA7108358', 'HCA7137567', 'HCA7175272', 'HCA7181873', 'HCA7186883', 'HCA7222558', 'HCA7226566', 'HCA7247574', 'HCA7251969', 'HCA7260869', 'HCA7326166', 'HCA7378993', 'HCA7388794', 'HCA7410559', 'HCA7440164', 'HCA7452272', 'HCA7453375', 'HCA7483182', 'HCA7492486', 'HCA7492991', 'HCA7495593', 'HCA7502059', 'HCA7512769', 'HCA7530670', 'HCA7541675', 'HCA7552478', 'HCA7553177', 'HCA7581081', 'HCA7625176', 'HCA7627786', 'HCA7636686', 'HCA7651278', 'HCA7664792', 'HCA7670989', 'HCA7705275', 'HCA7715581', 'HCA7716381', 'HCA7716684', 'HCA7717484', 'HCA7745994', 'HCA7764594', 'HCA7773393', 'HCA7777200', 'HCA7807384', 'HCA7825487', 'HCA7841485', 'HCA7885102', 'HCA7888815', 'HCA7898818', 'HCA7910680', 'HCA7941388', 'HCA7956199', 'HCA7962902', 'HCA7963196', 'HCA8038772', 'HCA8065472', 'HCA8066676', 'HCA8123460', 'HCA8141563', 'HCA8142767', 'HCA8169484', 'HCA8174679', 'HCA8219877', 'HCA8232061', 'HCA8251368', 'HCA8252471', 'HCA8296592', 'HCA8306569', 'HCA8335778', 'HCA8350976', 'HCA8358285', 'HCA8361577', 'HCA8363278', 'HCA8368490', 'HCA8369896', 'HCA8421569', 'HCA8435176', 'HCA8449490', 'HCA8463787', 'HCA8476190', 'HCA8481789', 'HCA8503167', 'HCA8511671', 'HCA8517582', 'HCA8532174', 'HCA8553485', 'HCA8578704', 'HCA8580690', 'HCA8596403', 'HCA8597405', 'HCA8626082', 'HCA8657295', 'HCA8699817', 'HCA8711477', 'HCA8712883', 'HCA8712883', 'HCA8751792', 'HCA8793607', 'HCA8797211', 'HCA8800274', 'HCA8854398', 'HCA8858912', 'HCA8867004', 'HCA8913388', 'HCA8927501', 'HCA9023865', 'HCA9044570', 'HCA9088388', 'HCA9095284', 'HCA9096690', 'HCA9157179', 'HCA9161877', 'HCA9166786', 'HCA9179997', 'HCA9187693', 'HCA9194084', 'HCA9196088', 'HCA9319280', 'HCA9319684', 'HCA9329081', 'HCA9339892', 'HCA9366895', 'HCA9377597', 'HCA9384089', 'HCA9392997', 'HCA9435080', 'HCA9455288', 'HCA9478098', 'HCA9481693', 'HCA9515684', 'HCA9521073', 'HCA9554088', 'HCA9578406', 'HCA9599212', 'HCA9601374', 'HCA9603681', 'HCA9614484', 'HCA9617793', 'HCA9626693', 'HCA9628697', 'HCA9640889', 'HCA9641386', 'HCA9646699', 'HCA9650993', 'HCA9662495', 'HCA9677509', 'HCA9686611', 'HCA9688312', 'HCA9703079', 'HCA9707289', 'HCA9708190', 'HCA9715187', 'HCA9716088', 'HCA9717999', 'HCA9735294', 'HCA9739808', 'HCA9743900', 'HCA9744194', 'HCA9750290', 'HCA9753094', 'HCA9760091', 'HCA9761497', 'HCA9769211', 'HCA9771703', 'HCA9787415', 'HCA9815595', 'HCA9845403', 'HCA9865005', 'HCA9866310', 'HCA9868920', 'HCA9880001', 'HCA9880405', 'HCA9894315', 'HCA9896218', 'HCA9912391', 'HCA9912492', 'HCA9913090', 'HCA9922091', 'HCA9926201', 'HCA9938309', 'HCA9938814', 'HCA9943504', 'HCA9947411', 'HCA9953406', 'HCA9986825', 'HCA9992517']

with open(args.subject_input, 'r') as file:
    subject_ids = [line.strip() for line in file if line.strip()]
    # if you have specified subject targets:
    if len(targets) != 0:
        #if you have specified subject targets:
        subject_ids = list(set(subject_ids) & set(targets))

if args.check_file_paths: #check file existence
    print("Checking file existence...")
    check_files(subject_ids, args.wm_dir, args.outside_dir, args.pas_dir, args.project_name)
else: # or generate meta file
    # Initialize the CSV file and headers
    output_file = args.output
    headers = [
        "subject_id",
        "pas_mask_file_path",
        "white_matter_mask_file_path",
        "grey_matter_mask_file_path",
    ]

    print("Generating meta_tracking file...")

    # Start processing
    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # Write the header row

        # Loop through subject IDs and populate the rows
        for subject_id in subject_ids:
            grey_matter_mask_file_path, white_matter_mask_file_path, pas_mask_file_path_a, pas_mask_file_path_b = filename_distributer(subject_id, args.wm_dir, args.outside_dir, args.pas_dir, args.project_name)
            if os.path.exists(pas_mask_file_path_b):
                pas_mask_file_path = pas_mask_file_path_b
            else:
                pas_mask_file_path = pas_mask_file_path_a

            # Write the row to the CSV file
            writer.writerow({
                "subject_id": subject_id,
                "pas_mask_file_path": pas_mask_file_path,
                "white_matter_mask_file_path": white_matter_mask_file_path,
                "grey_matter_mask_file_path": grey_matter_mask_file_path,
            })

    print(f"DONE: Meta_file_tracking file generated at: {output_file}")

