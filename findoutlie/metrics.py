""" Scan outlier metrics
"""

# Any imports you need
# +++your code here+++
import numpy as np
import nibabel as nib


def dvars(img):
    """ Calculate dvars metric on Nibabel image `img`

    The dvars calculation between two volumes is defined as the square root of
    (the mean of the (voxel differences squared)).

    Parameters
    ----------
    img : nibabel image

    Returns
    -------
    dvals : 1D array
        One-dimensional array with n-1 elements, where n is the number of
        volumes in `img`.
    """
    # Hint: remember 'axis='.  For example:
    # In [2]: arr = np.array([[2, 3, 4], [5, 6, 7]])
    # In [3]: np.mean(arr, axis=1)
    # Out[2]: array([3., 6.])

    img_data = img.get_fdata()
    n_voxels = np.prod(img_data.shape[:-1])
    img_data_reshaped = np.reshape(img_data, (n_voxels, img_data.shape[-1]))
    vol_diff = np.diff(img_data_reshaped, axis=1)

    return np.sqrt(np.mean(vol_diff ** 2, axis=0))

    # raise NotImplementedError('Code up this function')
