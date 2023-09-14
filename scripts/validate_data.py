""" Python script to validate data

Run as:

    python3 scripts/validate_data.py data
"""

import sys
import hashlib
import logging
import os
import glob
from pathlib import Path

from findoutlie.utils import validate_data

# Create and set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    # This function (main) called when this file run as a script.
    #
    # Get the data directory from the command line arguments
    if len(sys.argv) < 2:
        logger.error("Please give data directory on "
                     "command line")
        raise RuntimeError("Please give data directory on "
                           "command line")
    data_directory = sys.argv[1]
    # Call function to validate data in data directory
    validate_data(data_directory)


if __name__ == '__main__':
    # Python is running this file as a script, not importing it.
    main()
