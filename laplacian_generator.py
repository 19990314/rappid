import csv
import importlib
import argparse
import time
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from pandas.io.clipboard import paste
from scipy.ndimage import convolve, generate_binary_structure
import nibabel as nib
from lap_calculator import *

# Import the laplacian function from laplacian.py
#laplacian_module = importlib.import_module("laplacian")  # Ensure laplacian.py is in the same directory
#laplacian = getattr(laplacian_module, "laplacian_updated")

# Define the argument parser
parser = argparse.ArgumentParser(description="Process subjects using the laplacian function.")
parser.add_argument(
    "--input",
    default="meta_info_per_sub.csv",
    help="Path to the CSV file containing subject information. Default is 'meta_info_per_sub.csv'."
)
parser.add_argument(
    "--log",
    default="laplacian_log.csv",
    help="Path to save the log of processing times for each subject. Default is 'laplacian_log.csv'."
)

# Parse arguments
args = parser.parse_args()

# Read the CSV file
with open(args.input, mode="r") as file:
    reader = csv.DictReader(file)
    subjects = list(reader)

# Log file initialization
log_headers = ["subject_id", "time_used", "status"]
output_path = os.getcwd() + "/output_from_pipeline/"

with open(args.log, mode="w", newline="") as log_file:
    log_writer = csv.DictWriter(log_file, fieldnames=log_headers)
    log_writer.writeheader()

    # Process each subject
    for subject in subjects:
        sample = subject["subject_id"]

        outer_boudary = nib.load(subject["grey_matter_mask_file_path"])
        inner_boudary = nib.load(subject["pas_mask_file_path"])
        target = nib.load(subject["white_matter_mask_file_path"])

        print(f"Processing subject: {sample}")
        start_time = time.time()

        try:
            # seg: holds the original voxel data
            seg_out = np.array(outer_boudary.get_fdata())
            seg_in = np.array(inner_boudary.get_fdata())
            seg_target = np.array(target.get_fdata())

            # count voxels/pas
            unique_labels_in = np.unique(seg_in)
            counts = {label: np.sum(seg_in == label) for label in unique_labels_in}
            counts_df = pd.DataFrame(list(counts.items()), columns=["PAS index", "voxel count"])
            counts_df.to_csv("voxel_count_per_pas_"+sample+".csv", index=False)

            filtered_indices = counts_df.loc[counts_df["voxel count"] > 4, "PAS index"]
            pas_indices = filtered_indices.astype(int).tolist()
            laplacian_updated(output_path, sample, seg_out, seg_in, seg_target, pas_indices, target.affine,target.header, global_pas=True)

            # Record successful processing
            time_used = round(time.time() - start_time, 2)
            log_writer.writerow({"subject_id": sample, "time_used": time_used, "status": "success"})
            print(f"Subject {sample} processed successfully in {time_used} seconds.")

        except Exception as e:
            # Handle errors and log them
            log_writer.writerow({"subject_id": sample, "time_used": "N/A", "status": f"error: {str(e)}"})
            print(f"Error processing subject {sample}: {e}")

print(f"Processing completed. Log saved to {args.log}")