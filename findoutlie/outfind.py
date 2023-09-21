""" Module with routines for finding outliers
"""

from pathlib import Path
import nibabel as nib
import numpy as np
import numpy.linalg as npl

from utils import robust_rescaling, sort_eigenvalues, kurtosis_weights


def detect_outliers(fname):
    """Implementation of the PCout outliers detector algorithm.
    
    Parameters
    ----------
    fname : str
        Filename of the scan to test for outliers.
    
    """
    # Checks to run 
    assert isinstance(fname, str)
    fname = Path(fname).absolute()
    if fname.is_dir():
        raise ValueError(f"The file {fname} is a directory and not a file!")
    if not fname.exists():
        raise FileExistsError(f"The file {fname} does not exists.")
    # Data loading
    header_info = nib.load(fname).header
    ts_data = nib.load(fname).get_fdata()
    # Start of algorithm 
    # as explained in the paper:
    # "Finding multivariate outliers in fMRI time-serie sdata" by Magnotti et. al.
    
    # Phase 1: detection of location outliers
    X = ts_data
    X_star = robust_rescaling(X) # rescale the data
    # decompose the data to obtain eigenvectors and eigenvalues
    weighted_cov_matrix = np.cov(X_star, rowvar=False) # calculate the weighted covariance matrix
    # Compute the eigenvalues and eigenvectors
    W, V = npl.eig(weighted_cov_matrix) # W is eigenvalues and V is eigenvectors
    # Sort eigenvalues and eigenvectors in descending order
    W_sorted, V_sorted = sort_eigenvalues(W,V)
    # Calculate the cumulative explained variance ratio and find p_star (number of components explaining at least 99% of variance)
    expv_ratio = np.cumsum(eigenvalues) / np.sum(eigenvalues)
    p_star = np.argmax(expv_ratio >= 0.99) + 1
    # Retain only the top p_star eigenvectors and eigenvalues
    top_V = V_sorted[:, :p_star]
    top_W = W_sorted[:p_star]
    # Calculate Z matrix
    Z = X_star @ top_W
    # Rescale Z 
    Z_star = robust_rescaling(Z)
    # Compute robust kurtosis weights for each component
    kurt_weights = kurtosis_weights(Z_star)
    
    
    
    
    


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
        outlier_dict[fname] = outliers
    return outlier_dict
