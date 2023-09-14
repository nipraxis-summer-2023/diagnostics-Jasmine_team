""" Test file for the validate_data.py script in the scripts directory
"""
import pytest
from pathlib import Path

from ..utils import file_hash, validate_data

def test_file_hash():
    """Assert the test file has the expected SHA1 hash."""
    test_file = Path(__file__).parent / 'test_files' / 'test_sha.txt'
    sha1 = file_hash(test_file)
    assert isinstance(sha1, str)
    assert sha1 == 'c58c0f19b254c3246f20cfbe2ba568ae498970ae'


def test_file_hash_error():
    """Assert the file_hash function raises an error for non-existent file."""
    test_file = Path(__file__).parent / 'test_files' / 'test_sha128.txt'
    with pytest.raises(FileExistsError):
        file_hash(test_file)


def test_validate_data():
    """Assert the validate_data function works for test data."""
    data_directory = Path(__file__).parent / 'test_files'
    validate_data(data_directory)
    assert True
    
def test_validate_data_error():
    """Assert that the errors are raised."""
    data_directory = Path(__file__).parent / 'test_files2'
    with pytest.raises(FileExistsError):
        validate_data(data_directory)
    data_directory = Path(__file__).parent / 'test_files/group-xx'
    with pytest.raises(FileExistsError):
        validate_data(data_directory)
    