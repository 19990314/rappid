# Shuting Chen by 2024.12.10
# visualize the 3D distribution of PAS and its laplacian gradients

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter
from scipy.ndimage import median_filter
from scipy.ndimage import binary_dilation

def laplacian_visualization(t2_affine, mask_data, laplacian_file, pas_index, subject, global_laplacian=False):
    # laplacian vector file
    #laplacian_file = "/Users/chen/Desktop/code/HCA6002236_pas8.nii.gz"  # Replace with the correct file path
    #laplacian_file = "/Users/chen/Desktop/code/HCA6086470/HCA6086470_pas1.nii.gz"
    laplacian_nii = nib.load(laplacian_file)
    laplacian_data = np.array(laplacian_nii.get_fdata())
    check = laplacian_data.max()


    # =================== smoothing the Laplacian field ===================
    # gaussian
    sigma = 1  # Standard deviation for Gaussian kernel; adjust for more/less smoothing
    #laplacian_data = gaussian_filter(laplacian_data, sigma=sigma)

    # median filter
    #size = 1  # Size of the filtering kernel
    #laplacian_data = median_filter(laplacian_data, size=size)

    # Visualize or save the smoothed Laplacian field
    #plt.imshow(smoothed_grid[:, :, smoothed_grid.shape[2] // 2], cmap='viridis')


    # =================== get gradient and coords ===================
    # laplacian gradient
    gradient = np.gradient(laplacian_data)
    # dilate the voxels
    mask_in = mask_data == pas_index
    #dilated_mask = binary_dilation(mask_in)
    dilated_mask = binary_dilation(mask_in, iterations=1)
    surrounding_layer = dilated_mask & ~mask_in

    # Get the coordinates of the elements where mask_data == 1
    coords = np.argwhere(mask_in)
    x_pas = []
    y_pas = []
    z_pas = []

    for coord in coords:
        x_i, y_i, z_i = coord  # Unpack the coordinates
        x_pas.append(x_i)
        y_pas.append(y_i)
        z_pas.append(z_i)

    coords = np.argwhere(surrounding_layer)
    x_wrap = []
    y_wrap = []
    z_wrap = []
    lap_x = []
    lap_y = []
    lap_z = []
    for coord in coords:
        x_i, y_i, z_i = coord  # Unpack the coordinates
        x_wrap.append(x_i)
        y_wrap.append(y_i)
        z_wrap.append(z_i)
        lap_x.append(-gradient[0][x_i,y_i,z_i])
        lap_y.append(-gradient[1][x_i,y_i,z_i])
        lap_z.append(-gradient[2][x_i,y_i,z_i])


    # =================== visualization ===================
    # plot canvas
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # voxels
    scatter = ax.scatter(x_pas, y_pas, z_pas, cmap='viridis', c = "blue", s=50)
    scatter = ax.scatter(x_wrap, y_wrap, z_wrap, cmap='viridis', c = "#5baeff", s=30)

    # arrows
    ax.quiver(x_wrap, y_wrap, z_wrap, lap_x, lap_y,lap_z, length=0.3, color='#d65d48', linewidth=0.7)
    #cbar = fig.colorbar(scatter, ax=ax, shrink=0.5)
    #cbar.set_label('Values')

    # Set axis labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title(subject + "\nPAS #"+str(pas_index)+"\n1-voxel tube\nsmoothed by median filter (size = 1)")
    plt.show()

    # =================== output into PDFs ===================
    if global_laplacian:
        output_path = "/Users/chen/Desktop/code/output/"+subject+"_global_laplacian/"+subject+"_pas" + str(pas_index) + ".pdf"
        fig.savefig(output_path, format="pdf")
    else:
        output_path = "/Users/chen/Desktop/code/output/"+subject+"/"+subject+"_pas" + str(pas_index) + ".pdf"
        fig.savefig(output_path, format="pdf")


# ============================= inputs =============================
root_path = "/Users/chen/Desktop/code/data"
subject_id = "HCA6002236"
#subject_id = "HCA6086470"

# T2-weighted MRI file
t2_file = root_path + "/" + subject_id + "_data/PVS_" + subject_id + "_0001.nii.gz"
#t2_file = "/Users/chen/Desktop/code/HCA6086470_data/PVS_HCA6086470_0001.nii.gz"
t2_nii = nib.load(t2_file)
t2_data = t2_nii.get_fdata()
t2_affine = t2_nii.affine

# mask file for PAS
mask_file = root_path + "/" + subject_id + "_data/PVS_" + subject_id + "_instances.nii.gz"
#mask_file = "/Users/chen/Desktop/code/HCA6086470_data/PVS_HCA6086470_instances.nii.gz"
mask_nii = nib.load(mask_file)
mask_data = np.array(mask_nii.get_fdata())

global_laplacian = True
for i in range(1, 11):
    if global_laplacian:
        #laplacian_file = root_path + subject_id + "/" + subject_id + "_PAS_global_laplacian.nii.gz"
        laplacian_file = "/Users/chen/Desktop/code/output_from_pipeline/laplacian/HCA6002236_PAS_global_laplacian.nii.gz"
        #laplacian_file = "/Users/chen/Desktop/code/data/HCA6002236/HCA6002236_PAS_global_laplacian.nii.gz"
        laplacian_visualization(t2_affine, mask_data, laplacian_file, i, subject_id, global_laplacian)
    else:
        laplacian_file = root_path + subject_id + "/" + subject_id + "_pas" + str(i)+ ".nii.gz"
        laplacian_visualization(t2_affine, mask_data, laplacian_file, i, subject_id, global_laplacian)
