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
import pandas as pd
from sklearn.decomposition import PCA


def get_laplacian_gradient(laplacian_file):
    # =================== read  laplacian field file ===================
    laplacian_nii = nib.load(laplacian_file)
    laplacian_data = np.array(laplacian_nii.get_fdata())

    # =================== smoothing the Laplacian field ===================
    # gaussian
    #sigma = 1  # Standard deviation for Gaussian kernel; adjust for more/less smoothing
    # laplacian_data = gaussian_filter(laplacian_data, sigma=sigma)

    # median filter
    # size = 1  # Size of the filtering kernel
    # laplacian_data = median_filter(laplacian_data, size=size)

    # Visualize or save the smoothed Laplacian field
    # plt.imshow(smoothed_grid[:, :, smoothed_grid.shape[2] // 2], cmap='viridis')

    # =================== return gradient vector ===================
    return np.gradient(laplacian_data)


def get_voxel_indices(file_path, min_vox):
    # Read the voxel ct file
    ct = pd.read_csv(file_path)

    # Filter rows where voxel count > 4
    return ct[(ct["voxel count"] > min_vox) & (ct["PAS index"] != 0)]["PAS index"].tolist()


def extract_perpendicular_vectors(mask_data, pas_index, gradient):
    x_pas = []
    y_pas = []
    z_pas = []
    x_wrap = []
    y_wrap = []
    z_wrap = []
    lap_x = []
    lap_y = []
    lap_z = []

    for i in pas_index:
        PVS_volume = np.zeros(mask_data.shape)
        PVS_volume[mask_data == i] = 1
        dilated_mask = binary_dilation(PVS_volume, iterations=1)
        surrounding_layer = dilated_mask - PVS_volume

        # process the pas voxels
        coords = np.argwhere(PVS_volume)
        for coord in coords:
            x_i, y_i, z_i = coord  # Unpack the PVS coordinates
            x_pas.append(x_i)
            y_pas.append(y_i)
            z_pas.append(z_i)

        PVS_label = np.nonzero(mask_data == i)
        pvs_indices = np.asarray(PVS_label)
        pvs_coords = pvs_indices.T
        pca = PCA(n_components=3)
        pca.fit(pvs_coords)
        # Get the first principal component
        first_pc = pca.components_[0]

        # process the 1-voxel-away space
        coords = np.argwhere(surrounding_layer)
        for coord in coords:
            x_i, y_i, z_i = coord
            x_wrap.append(x_i)
            y_wrap.append(y_i)
            z_wrap.append(z_i)
            lap_vec = np.array([
                -gradient[0][x_i, y_i, z_i],
                -gradient[1][x_i, y_i, z_i],
                -gradient[2][x_i, y_i, z_i]
            ]) # Compute Laplacian components
            magnitude = np.linalg.norm(lap_vec) # calculate magnitute of the vector
            if magnitude > 1e-6:  # Avoid division by zero
                lap_vec_unit = lap_vec / magnitude # Make it a unit vector
            else:
                lap_vec_unit = np.array([0.0, 0.0, 0.0])  # Handle zero-magnitude case

            # vector angle thresholds
            cos_lower = -np.sqrt(2) / 2  # -0.707
            cos_upper =  np.sqrt(2) / 2  #  0.707
            # calculate the angels
            cos_theta = np.dot(first_pc, lap_vec_unit)

            if cos_lower <= cos_theta <= cos_upper:
                #print(f"The angle between first_pc and lap_vec_unit is within the range [{np.arccos(cos_upper)}, {np.arccos(cos_lower)}] radians.")
                lap_x.append(-gradient[0][x_i, y_i, z_i])
                lap_y.append(-gradient[1][x_i, y_i, z_i])
                lap_z.append(-gradient[2][x_i, y_i, z_i])
            else:
                lap_x.append(0)
                lap_y.append(0)
                lap_z.append(0)
    return x_pas, y_pas, z_pas, x_wrap, y_wrap, z_wrap, lap_x, lap_y, lap_z


def laplacian_visualization(mask_data, laplacian_file, pas_index, subject, plot_settings):
    # calculate gradient
    gradient = get_laplacian_gradient(laplacian_file)

    # get the pas masks
    if plot_settings["global_laplacian"]:
        mask_in = np.isin(mask_data, pas_index) # a list of PASs
    else:
        mask_in = mask_data == pas_index # single pas

    # dilate the voxels
    #dilated_mask = binary_dilation(mask_in)
    dilated_mask = binary_dilation(mask_in, iterations=1)
    surrounding_layer = dilated_mask & ~mask_in

    # Get the coordinates of the pas voxels
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

    # if we need to filter vectors by angles
    if plot_settings["FLAG_filter_by_angles"]:
        x_pas, y_pas, z_pas, x_wrap, y_wrap, z_wrap, lap_x, lap_y, lap_z = extract_perpendicular_vectors(mask_data, pas_index, gradient)


    # =================== visualization ===================
    # plot canvas
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # voxels
    scatter = ax.scatter(x_pas, y_pas, z_pas, cmap='viridis', c = "blue", s=plot_settings["pas_voxel_size"]) #change s
    scatter = ax.scatter(x_wrap, y_wrap, z_wrap, cmap='viridis', c = "#5baeff", s=plot_settings["boarder_voxel_size"]) #change s

    # arrows
    ax.quiver(x_wrap, y_wrap, z_wrap, lap_x, lap_y,lap_z, length=plot_settings["arrow_len"], color='#d65d48', linewidth=plot_settings["arrow_width"])
    #cbar = fig.colorbar(scatter, ax=ax, shrink=0.5)
    #cbar.set_label('Values')

    # Set axis labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title(plot_settings["title"])
    plt.show()

    # =================== output into PDFs ===================
    if plot_settings["global_laplacian"]:
        output_path = "/Users/chen/Desktop/code/output/"+subject+"_global_laplacian/"+subject+"_pas" + str(pas_index) + ".pdf"
        #fig.savefig(output_path, format="pdf")
    else:
        output_path = "/Users/chen/Desktop/code/output/"+subject+"/"+subject+"_pas" + str(pas_index) + ".pdf"
        #fig.savefig(output_path, format="pdf")


# ============================= inputs =============================
root_path = "/Users/chen/Desktop/code/data"
subject_id = "HCA6002236"
#subject_id = "HCA6086470"

# T2-weighted MRI file
#t2_file = root_path + "/" + subject_id + "_data/PVS_" + subject_id + "_0001.nii.gz"
#t2_file = "/Users/chen/Desktop/code/HCA6086470_data/PVS_HCA6086470_0001.nii.gz"
#t2_nii = nib.load(t2_file)
#t2_data = t2_nii.get_fdata()
#t2_affine = t2_nii.affine

# mask file for PAS
#mask_file = root_path + "/" + subject_id + "_data/PVS_" + subject_id + "_instances.nii.gz"
mask_file = "/Users/chen/Downloads/PVS_HCA6002236_ref_labels_instances.nii.gz"
mask_nii = nib.load(mask_file)
mask_data = np.array(mask_nii.get_fdata())

# plot parameters
#title = subject_id + "\nPAS #"+str(pas_index)+"\n1-voxel tube\nsmoothed by median filter (size = 1)"
plot_settings = {
    "global_laplacian": True,
    "pas_voxel_size": 5,
    "boarder_voxel_size": 3,
    "arrow_len": 0.9,
    "arrow_width": 0.4,
    "title": subject_id + "\nall the PASs with voxels > 4",
    "FLAG_filter_by_angles": True
}

if plot_settings["global_laplacian"]:
    # laplacian_file = root_path + subject_id + "/" + subject_id + "_PAS_global_laplacian.nii.gz"
    laplacian_file = "/Users/chen/Desktop/code/output_from_pipeline/laplacian/HCA6002236_PAS_global_laplacian.nii.gz"
    # laplacian_file = "/Users/chen/Desktop/code/data/HCA6002236/HCA6002236_PAS_global_laplacian.nii.gz"
    file_path = "/Users/chen/Desktop/code/output_from_pipeline/laplacian/voxel_count_per_pas_HCA6002236.csv"  # Replace with the path to your CSV file
    pas_indices = get_voxel_indices(file_path, min_vox = 4)

    # plot
    laplacian_visualization(mask_data, laplacian_file, pas_indices, subject_id, plot_settings)
    plot_settings["title"] = subject_id + "\nthe first 8 PASs ordered by voxel count"
    laplacian_visualization(mask_data, laplacian_file, [1, 2, 3, 4, 5, 6, 7, 8], subject_id, plot_settings)
else:
    for i in range(1, 2):
        laplacian_file = root_path + subject_id + "/" + subject_id + "_pas" + str(i)+ ".nii.gz"
        laplacian_visualization(mask_data, laplacian_file, i, subject_id, plot_settings)

