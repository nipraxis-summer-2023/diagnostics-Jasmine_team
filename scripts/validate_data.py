""" Python script to validate data

Run as:

    python3 scripts/validate_data.py data
"""

import sys
import hashlib
import os
import glob
from pathlib import Path


def file_hash(filename):
    """ Get byte contents of file `filename`, return SHA1 hash

    Parameters
    ----------
    filename : str
        Name of file to read

    Returns
    -------
    hash : str
        SHA1 hexadecimal hash string for contents of `filename`.
    """
    # Open the file, read contents as bytes.
    pth_filename = Path(filename)
    filename_bytes = pth_filename.read_bytes()
    # Calculate, return SHA1 has on the bytes from the file.
    sha1_filename = hashlib.sha1(filename_bytes).hexdigest()

    return sha1_filename


def validate_data(data_directory):
    """ Read ``data_hashes.txt`` file in `data_directory`, check hashes

    Parameters
    ----------
    data_directory : str
        Directory containing data and ``data_hashes.txt`` file.

    Returns
    -------
    None

    Raises
    ------
    ValueError:
        If hash value for any file is different from hash value recorded in
        ``data_hashes.txt`` file.
    """

    # Change th directory to data_directory
    os.chdir(data_directory)
    data_path = Path(data_directory)
    file_hash_to_open = data_path / 'group-00/hash_list.txt'
    # Read lines from ``data_hashes.txt`` file.
    with open(file_hash_to_open, 'r') as f:
        lines = f.read().split('\n')
    for i in range(0, len(lines)-1):
        # Split into SHA1 hash and filename
        line = lines[i].split()
        SHA_1 = line[0]
        filename = line[1]
        # Calculate actual hash for given filename.
        hash_filename = file_hash(filename)
        if SHA_1 != hash_filename:
            raise NotImplementedError('Hash for filename is not the same as the one in the file')

    # If hash for filename is not the same as the one in the file, raise
    # ValueError
    # This is a placeholder, replace it to write your solution.
    # raise NotImplementedError('This is just a template -- you are expected to code this.')


def main():
    # This function (main) called when this file run as a script.
    #
    # Get the data directory from the command line arguments
    if len(sys.argv) < 2:
        raise RuntimeError("Please give data directory on "
                           "command line")
    data_directory = sys.argv[1]
    # Call function to validate data in data directory
    validate_data(data_directory)


if __name__ == '__main__':
    # Python is running this file as a script, not importing it.
    main()
