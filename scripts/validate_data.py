""" Python script to validate data

Run as:

    python3 scripts/validate_data.py data
"""

from pathlib import Path
import sys
import hashlib

def file_hash(filename: str) -> str:
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
    # Calculate, return SHA1 has on the bytes from the file.
    filename = Path(filename)
    # Assert the file exists, if not raise an error
    if not filename.exists():
        raise FileExistsError(f'File {filename} does not exist')
    # Read the file as bytes and return SHA1 hash
    return hashlib.sha1(filename.read_bytes()).hexdigest()
    

def validate_data(data_directory: str) -> None:
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
    # Read lines from ``hash_lists.txt`` file.
    # Split into SHA1 hash and filename
    # Calculate actual hash for given filename.
    # If hash for filename is not the same as the one in the file, raise
    # ValueError
    data_directory = Path(data_directory)
    if not data_directory.exists():
        raise FileExistsError(f'Directory {data_directory} does not exist')
    if not data_directory.is_dir():
        raise NotADirectoryError(f'{data_directory} is not a directory')
    # Read the data_hashes.txt file
    data_hashes = next(data_directory.rglob('group-*/hash_list.txt'), None)
    print(data_hashes)
    if not data_hashes.exists():
        raise FileExistsError(f'{data_hashes} does not exist')
    # Loop through the lines of the data_hashes.txt file. The file contents are composed as:
    # hash1 filename. Split and use the file_hash function to calculate the hash of the filename.
    for line in data_hashes.read_text().splitlines():
        hash1, filename = line.split()
        hash2 = file_hash(data_directory / filename)
        if hash1 != hash2:
            raise ValueError(f'Hash mismatch for {filename}: '
                             f'{hash1} != {hash2}')                     
        else:
            print(f'Hash match for {filename}: {hash1} == {hash2}')
    return


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
