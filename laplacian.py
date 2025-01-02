# Cong Zang, 02/01/2024
# Calculate Laplacian (Electric) Potential given a segmentation mask, with
# 3 represents outer boundary, 2 represents inside the mask and 1 represents
# inner boundary.
# inspired by https://github.com/lukepolson/youtube_channel/blob/main/Python%20Metaphysics%20Series/vid31.ipynb


# ========= packages =========
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.io.clipboard import paste
from scipy.ndimage import convolve, generate_binary_structure
import nibabel as nib
import plotly.graph_objects as go
import argparse

# ========= original code by Con =========
#ID = pd.read_table('./srcs/train.txt',header=None).values.reshape(-1)
def laplacian():
    # id = str(ID[i])
    # GenerateMask(id)
    # PATH1 = '/ifs/loni/faculty/hkim/cong/WMH/civet/output/'
    # PATH1 = '/scratch/faculty/hkim/cong/data/ukbb/civet/wm_BAP/'
    # Seg = nib.load(PATH1+str(id)+'/final/nii/lap_mask_L.nii')
    # Seg = nib.load(PATH1+str(id)+'/lap_mask_L.nii')
    Seg = nib.load("/HCA6086470_data/HCA6086470_outside3.nii.gz")

    # grid and seg: holds the voxel data to process.
    seg = np.array(Seg.get_fdata())
    grid = np.array(Seg.get_fdata())
    I,J,K = grid.shape
    xv, yv, zv = np.meshgrid(np.arange(I),np.arange(J),np.arange(K))

    # kernel
    kern = generate_binary_structure(3,1).astype(float)/6
    kern[1,1,1] = 0

    # sphere to GM surface
    mask_out = seg ==3 # outside white mater == grey matter + brain boarder
    grid[mask_out]=0
    mask_in = seg==1 # within pas
    grid[mask_in]=10
    mask_lap = seg==2 # target for laplacian = white mater
    grid[mask_lap]=5
    mask_lap_sum = np.sum(mask_lap)
    err = []
    iters = 0
    err_i=100000

    # def: 5000
    while iters<=100:
        grid_updated = convolve(grid,kern, mode='constant')
        # Boundary conditions (neumann)
        # grid_updated = neumann(grid_updated)
        # Boundary conditions (dirchlett)
        grid_updated[mask_out] = 0
        grid_updated[mask_in] = 10
        # See what error is between consecutive arrays
        err_i = np.sum((grid-grid_updated)**2)/mask_lap_sum
        print(iters,err_i)
        err.append(err_i)
        grid = grid_updated
        iters+=1
    print('finished')

    img_lap = nib.Nifti1Image(grid.reshape(I,J,K).astype(np.float32),Seg.affine,Seg.header)
    # nib.save(img_lap,PATH1+id+f'/Laplacian_L_new.nii')
    print("done")
    nib.save(img_lap, "HCA6002236_labeled_pas1.nii.gz")

# ========= file info =========
# exact: white mater only
# ins: pvs (0-n) ======> [inner boundary]
# 0001: visualize (t2)

# Dec 02 new files:
# wm_2.gz: target ======> [target]
# outside3: out boundary ======> [out boundary]

# Code modified code by Shuting
def laplacian_updated(root_path, sample, seg_out, seg_in, seg_target, pas_index, affine, header, global_pas):
    # grid: update laplacian vectors
    grid = seg_in

    # check labels
    # unique_labels_out = np.unique(seg_out)
    #print("Segmentation labels:", len(unique_labels_out))
    # nique_labels_in = np.unique(seg_in)
    # test = np.count_nonzero(seg_in)
    #print("Unique segmentation labels:", len(unique_labels_in))
    # unique_labels_target = np.unique(seg_target)
    #print("Unique segmentation labels:", len(unique_labels_target))

    I,J,K = grid.shape
    #xv, yv, zv = np.meshgrid(np.arange(I),np.arange(J),np.arange(K))

    # kernel
    kern = generate_binary_structure(3,1).astype(float)/6
    kern[1,1,1] = 0

    # sphere to GM surface
    # outside white mater == grey matter + brain boarder
    #mask_out = (seg_out == 0) | (seg_out == 2) | (seg_out == 3) | (seg_out == 4)
    mask_out = (seg_out == 3) | (seg_out == 4)
    #mask_out = (seg_out == 0) | (seg_out == 1) |(seg_out == 2) | (seg_out == 3) | (seg_out == 4) | (seg_out == 5) |(seg_out == 6)
    grid[mask_out]=0

    if global_pas:
        mask_in = np.isin(seg_in, pas_index)
    else:
        mask_in = seg_in == pas_index # pas
    #coords = np.argwhere(mask_in)
    grid[mask_in]=10

    # target for laplacian = white mater
    mask_lap = (seg_target == 0) | (seg_target == 1) | (seg_target == 2) | (seg_target == 3) | (seg_target == 4) | (seg_target == 5) | (seg_target == 6)
    grid[mask_lap]=5

    mask_lap_sum = np.sum(mask_lap)
    err = []
    iters = 0
    err_i=100000

    while iters<=5:
        grid_updated = convolve(grid,kern, mode='constant')
        # Boundary conditions (neumann)
        # grid_updated = neumann(grid_updated)
        # Boundary conditions (dirchlett)
        grid_updated[mask_out] = 0
        grid_updated[mask_in] = 10
        # See what error is between consecutive arrays
        err_i = np.sum((grid-grid_updated)**2)/mask_lap_sum
        print(iters,err_i)
        err.append(err_i)
        grid = grid_updated
        iters+=1

    img_lap = nib.Nifti1Image(grid.reshape(I,J,K).astype(np.float32), affine,header)
    # nib.save(img_lap,PATH1+id+f'/Laplacian_L_new.nii')
    #print("PAS #" + str(pas_index) + ": done")
    if global_pas:
        nib.save(img_lap, root_path+sample+"/"+sample+"_PAS_global_laplacian.nii.gz")
    else:
        nib.save(img_lap, root_path+sample+"/"+sample+"_pas"+str(pas_index)+".nii.gz")





# main script
import time
root_path = "//"
sample = "HCA6002236"


outer_boudary = nib.load(root_path + sample + "_data/"+ sample + "_outside3.nii.gz")  # 0 2 3 4
inner_boudary = nib.load(root_path +  sample + "_data/"+ "PVS_"+ sample + "_instances.nii.gz")  # 0-340
#target = nib.load(root_path + "HCA6002236_data/" + sample + "_pve_exactwm_2.nii.gz")  # 0 1 2 3 4 5 6
target = nib.load(root_path + "HCA6002236_data/" + sample + "_wm_2.nii.gz")  # 0 1 2 3 4 5 6

# seg: holds the original voxel data
seg_out = np.array(outer_boudary.get_fdata())
seg_in = np.array(inner_boudary.get_fdata())
seg_target = np.array(target.get_fdata())

# count pas voxels
unique_labels_in = np.unique(seg_in)
counts = {label: np.sum(seg_in == label) for label in unique_labels_in}
counts_df = pd.DataFrame(list(counts.items()), columns=["PAS index", "voxel count"])
#counts_df.to_csv("voxel_count_per_pas_"+sample+".csv", index=False)

# -
filtered_indices = counts_df.loc[counts_df["voxel count"] > 4, "PAS index"]
pas_indices = filtered_indices.astype(int).tolist()
#laplacian_updated(root_path, sample, seg_out, seg_in, seg_target, pas_indices[1:], target.affine,target.header, global_pas=True)
#exit()

timings = []
for i in range(2,11):
    start = time.time()
    laplacian_updated(root_path, sample, seg_out, seg_in, seg_target, i, target.affine,target.header, global_pas=False)
    end = time.time()
    execution_time = end - start
    timings.append({"PAS": f"PAS {i}", "Execution Time (s)": execution_time})
    exit()

# Store the timings in a pandas DataFrame
#time_record_df = pd.DataFrame(timings)
#time_record_df.to_csv("time_record_subject2.csv", index=False)

