#subject_id,
#pas_mask_file_path,
#white_matter_mask_file_path,
#grey_matter_mask_file_path,


import argparse
import csv
import time
import os

subject_file_path = "/ifs/loni/faculty/hkim/hedong/DTI_NODDI/listfile/HCA_625ascend.txt"
wm_dir = "/ifs/loni/faculty/hkim/yaqiong/HCP-A-CIVET2/"
outside_dir = "/ifs/loni/faculty/hkim/yaqiong/HCP-A-CIVET2/"
pas_dir = "/ifs/loni/faculty/hkim/hedong/HCP_A_PVS_label/prediction_label/PVS_instance_3_396/"
output_file = "/ifs/loni/faculty/hkim/shuting/code/output_from_pipeline/meta_file_tracker.csv"

def check_files(subject_ids, wm_dir, outside_dir, pas_dir):
    """
    Check the existence of required files for each subject ID.

    Args:
        subject_ids (a list of str): subject IDs.
        dir (str): Base directory where the files are located.

    Returns:
        None
    """
    # Read the subject IDs from the text file

    # Initialize a list to collect error messages
    errors = []

    # Loop through each subject ID
    for subject_id in subject_ids:
        # Define the expected file paths
        file1 = os.path.join(outside_dir, f"{subject_id}_V1_MR/{subject_id}_outside3_final.nii.gz")
        file2 = os.path.join(wm_dir, f"{subject_id}_V1_MR/{subject_id}_wm_2.nii.gz")
        file3a = os.path.join(pas_dir, f"PVS_{subject_id}_instances.nii.gz")
        file3b = os.path.join(pas_dir, f"PVS_{subject_id}_ref_labels_instances.nii.gz")

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


# Define the command-line argument parser
parser = argparse.ArgumentParser(description="Generate a CSV file with subject information.")
parser.add_argument(
    "--output",
    default=output_file,
    help="Path to save the output CSV file. Default is 'output.csv'."
)
parser.add_argument(
    "--subject_input",
    default=subject_file_path,
    help="Path to save the subject file.."
)
parser.add_argument(
    "--wm_dir",
    default=wm_dir,
    help="Path to save the wm file.."
)
parser.add_argument(
    "--outside_dir",
    default=outside_dir,
    help="Path to save the outside file.."
)
parser.add_argument(
    "--pas_dir",
    default=pas_dir,
    help="Path to save the pas file.."
)
parser.add_argument(
    "--check_file_paths",
    action='store_true',
    help="Flag to check files"
)

print("Reading inputs...")
# Parse the command-line arguments
args = parser.parse_args()
with open(args.subject_input, 'r') as file:
    subject_ids = [line.strip() for line in file if line.strip()]

if args.check_file_paths:
    print("Checking file existence...")
    #check file existence
    check_files(subject_ids, args.wm_dir, args.outside_dir, args.pas_dir)
else:
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
            grey_matter_mask_file_path = os.path.join(outside_dir, f"{subject_id}_V1_MR/{subject_id}_outside3_final.nii.gz")
            white_matter_mask_file_path = os.path.join(wm_dir, f"{subject_id}_V1_MR/{subject_id}_wm_2.nii.gz")
            pas_mask_file_path_a = os.path.join(pas_dir, f"PVS_{subject_id}_instances.nii.gz")
            pas_mask_file_path_b = os.path.join(pas_dir, f"PVS_{subject_id}_ref_labels_instances.nii.gz")

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

