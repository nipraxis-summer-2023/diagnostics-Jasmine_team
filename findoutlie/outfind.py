""" Module with routines for finding outliers
"""

from pathlib import Path
import nibabel as nib
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def detect_outliers(fname):

    # Load image and get the data
    img = nib.load(fname)
    data = img.get_fdata()

    # Calculate variance within each 3D volume
    variance = np.zeros(data.shape[-1])
    for i in range(0, data.shape[-1]):

        curr_data = data[:, :, :, i]
        n_voxels = np.prod(curr_data.shape[:-1])
        # Reshape the data of volume [n_voxels_per_slice, number_of_slices]
        img_data_reshaped = np.reshape(curr_data, (n_voxels, curr_data.shape[-1]))

        # Prepare the data for PCA
        df_data = pd.DataFrame(img_data_reshaped)
        feat_cols = ['Slice_' + str(i) for i in range(df_data.shape[1])]

        # Standardize the data
        x = df_data.loc[:, :].values
        y = StandardScaler().fit_transform(x)

        # PCA
        pca = PCA(n_components=2)
        principalComponents = pca.fit_transform(x)
        principal_Df = pd.DataFrame(data=principalComponents,
                                    columns=['principal component 1', 'principal component 2'])
        variance[i] = pca.explained_variance_ratio_[0]

    variance = variance.tolist()
    variance_mean = np.mean(variance, axis=0)
    variance_std = np.std(variance, axis=0)

    # Find variance_outliers using mean and standard deviation
    variance_outliers = [variance_volume for variance_volume in variance if (variance_volume < variance_mean - 2 * variance_std)]
    variance_outliers = [variance_volume for variance_volume in variance if (variance_volume > variance_mean + 2 * variance_std)]
    volume_outliers = [variance.index(i) for i in variance_outliers]

    return volume_outliers


def find_outliers(data_directory):
    """ Return filenames and outlier indices for images in `data_directory`.

    Parameters
    ----------
    data_directory : str
        Directory containing containing images.

    Returns
    -------
    outlier_dict : dict
        Dictionary with keys being filenames and values being lists of outliers
        for filename.
    """
    image_fnames = Path(data_directory).glob('**/sub-*.nii.gz')
    outlier_dict = {}
    for fname in image_fnames:
        outliers = detect_outliers(fname)
        outlier_dict[str(fname)] = outliers
    return outlier_dict
