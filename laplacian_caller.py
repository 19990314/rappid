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

# Import the laplacian function from lap_calculator.py
#laplacian_module = importlib.import_module("laplacian")  # Ensure laplacian.py is in the same directory
#laplacian = getattr(laplacian_module, "laplacian_updated")

# Define the argument parser
parser = argparse.ArgumentParser(description="Process subjects using the laplacian function.")
parser.add_argument(
    "--sample",
    default="NA",
    help="Path to the CSV file containing subject information. Please check through '/ifs/loni/faculty/hkim/shuting/code/output_from_pipeline/meta_file_tracker.csv'."
)

parser.add_argument(
    "--meta",
    default='/ifs/loni/faculty/hkim/shuting/code/output_from_pipeline/meta_file_tracker2.csv',
    help="Path to the CSV file containing subject information. Please check through '/ifs/loni/faculty/hkim/shuting/code/output_from_pipeline/meta_file_tracker.csv'."
)
parser.add_argument(
    "--time_book",
    default="time_book2.csv",
    help="Path to save the log of processing times for each subject. Default is 'time_book.csv'."
)
parser.add_argument(
    "--output_dir",
    default="/ifs/loni/faculty/hkim/shuting/code/output_from_pipeline/",
    help="Path to save the laplacian fields"

)
parser.add_argument(
    "--laplacian_dir_name",
    default="laplacian/",
    help="Path to save the laplacian fields"

)

# Parse arguments
args = parser.parse_args()
output_path = args.output_dir + args.laplacian_dir_name
subjects = pd.read_csv(args.meta)
row = subjects[subjects["subject_id"] == args.sample]

#calculate
sample = str(row["subject_id"].iloc[0])
outer_boudary = nib.load(str(row["grey_matter_mask_file_path"].iloc[0]))
inner_boudary = nib.load(str(row["pas_mask_file_path"].iloc[0]))
target = nib.load(str(row["white_matter_mask_file_path"].iloc[0]))

print(f"Processing subject: {sample}...")
start_time = time.time()
# Open the file in append mode
try:
    # seg: holds the original voxel data
    seg_out = np.array(outer_boudary.get_fdata())
    seg_in = np.array(inner_boudary.get_fdata())
    seg_target = np.array(target.get_fdata())

    # count voxels per pas
    unique_labels_in = np.unique(seg_in)  # seg_in: the T2 data saved in Numpy obj
    counts = {label: np.sum(seg_in == label) for label in unique_labels_in}  # count voxels for each pas
    counts_df = pd.DataFrame(list(counts.items()), columns=["PAS index", "voxel count"])
    counts_df.to_csv(args.output_dir+"voxel_counts/" + "voxel_count_per_pas_" + sample + ".csv", index=False)  # output counts

    # keep PASs larger than 4-voxels
    counts_df = counts_df[counts_df["PAS index"] != 0]
    filtered_indices = counts_df.loc[counts_df["voxel count"] > 4, "PAS index"]
    pas_indices = filtered_indices.astype(int).tolist()  # get the PAS labels, save into a list

    # calculate laplacian field
    laplacian_updated(output_path, sample, seg_out, seg_in, seg_target, pas_indices, target.affine, target.header,
                      global_pas=True)

    # Record successful processing
    time_used = round(time.time() - start_time, 2)
    with open(args.output_dir + args.time_book, "a") as file:
        file.write(str(args.sample) + "," + str(time_used) + "," + "success\n")
    print(f"{args.sample} done.")

except Exception as e:
    # Handle errors and log them
    with open(args.output_dir + args.time_book, "a") as file:
        file.write(str(args.sample) + ",-," + "fail\n")
    print(f"Error processing subject {args.sample}: {e}")
