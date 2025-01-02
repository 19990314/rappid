#subject_id,
#pas_mask_file_path,
#white_matter_mask_file_path,
#grey_matter_mask_file_path,


import argparse
import csv
import time

# Define the command-line argument parser
parser = argparse.ArgumentParser(description="Generate a CSV file with subject information.")
parser.add_argument(
    "subject_ids",
    nargs="+",
    help="List of subject IDs (space-separated) to process."
)
parser.add_argument(
    "--output",
    default="output.csv",
    help="Path to save the output CSV file. Default is 'output.csv'."
)

# Parse the command-line arguments
args = parser.parse_args()

# Initialize the CSV file and headers
output_file = args.output
headers = [
    "subject_id",
    "pas_mask_file_path",
    "white_matter_mask_file_path",
    "grey_matter_mask_file_path",
    "visualization_path",
    "time_used"
]

# Start processing
with open(output_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()  # Write the header row

    # Loop through subject IDs and populate the rows
    for subject_id in args.subject_ids:
        start_time = time.time()

        # Initialize placeholders for the paths (to be filled inside the loop)
        pas_mask_file_path = f"/path/to/pas_mask/{subject_id}_pas_mask.nii.gz"
        white_matter_mask_file_path = f"/path/to/white_matter/{subject_id}_wm_mask.nii.gz"
        grey_matter_mask_file_path = f"/path/to/grey_matter/{subject_id}_gm_mask.nii.gz"
        visualization_path = f"/path/to/visualization/{subject_id}_vis.png"

        # Simulate processing time for each subject
        time_used = time.time() - start_time

        # Write the row to the CSV file
        writer.writerow({
            "subject_id": subject_id,
            "pas_mask_file_path": pas_mask_file_path,
            "white_matter_mask_file_path": white_matter_mask_file_path,
            "grey_matter_mask_file_path": grey_matter_mask_file_path,
            "visualization_path": visualization_path,
            "time_used": round(time_used, 2)
        })

print(f"CSV file generated at: {output_file}")

