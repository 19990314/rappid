import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.io.clipboard import paste
from scipy.ndimage import convolve, generate_binary_structure
import nibabel as nib
import plotly.graph_objects as go
import argparse
import os

#HCA6002236,/Users/chen/Downloads/PVS_HCA6002236_ref_labels_instances.nii.gz,/Users/chen/Downloads/HCA6002236_wm_2.nii.gz,/Users/chen/Downloads/HCA6002236_outside3_final.nii.gz


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
    mask_out = seg_out == 3
    #mask_out = (seg_out == 0) | (seg_out == 1) |(seg_out == 2) | (seg_out == 3) | (seg_out == 4) | (seg_out == 5) |(seg_out == 6)
    grid[mask_out]=0

    if global_pas:
        mask_in = np.isin(seg_in, pas_index)
    else:
        mask_in = seg_in == pas_index # pas
    #coords = np.argwhere(mask_in)
    grid[mask_in]=10

    # target for laplacian = white mater
    #mask_lap = (seg_target == 0) | (seg_target == 1) | (seg_target == 2) | (seg_target == 3) | (seg_target == 4) | (seg_target == 5) | (seg_target == 6)
    mask_lap = seg_target == 2
    grid[mask_lap] = 5

    mask_lap_sum = np.sum(mask_lap)
    err = []
    iters = 0
    err_i = 100000

    while iters<=5000:
        grid_updated = convolve(grid,kern, mode='constant')
        # Boundary conditions (neumann)
        # grid_updated = neumann(grid_updated)
        # Boundary conditions (dirchlett)
        grid_updated[mask_out] = 0
        grid_updated[mask_in] = 10
        # See what error is between consecutive arrays
        err_i = np.sum((grid-grid_updated)**2)/mask_lap_sum
        #print(iters,err_i)
        err.append(err_i)
        grid = grid_updated
        iters+=1

    img_lap = nib.Nifti1Image(grid.reshape(I,J,K).astype(np.float32), affine,header)
    # nib.save(img_lap,PATH1+id+f'/Laplacian_L_new.nii')
    #print("PAS #" + str(pas_index) + ": done")

    if global_pas:
        laplacian_output_file_path = root_path+sample+"_PAS_global_laplacian.nii.gz"
    else:
        laplacian_output_file_path = root_path+sample+"_pas"+str(pas_index)+".nii.gz"

    nib.save(img_lap, laplacian_output_file_path)
    print(f"{sample}: laplacian done, file saved at : {laplacian_output_file_path}")
    file_size = os.path.getsize(laplacian_output_file_path)
    file_size_mb = file_size / (1024 * 1024) #MB format
    print(f"{sample}: laplacian done, file saved at : {laplacian_output_file_path}, file size: {file_size_mb:.2f} MB")
