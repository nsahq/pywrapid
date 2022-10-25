#!/usr/bin/python3
"""
Collection of file helper functions
"""
import os


def is_file_readable(path: str) -> bool:
    """Checks a file in a given path to make sure it:
        - exists
        - is a file
        - is readable
        - is not an empty file

    Args:
        path (str): Path to configuration file.

    Returns:
        bool: True/False.
    """
    if (
        os.path.exists(path)
        and os.path.isfile(path)
        and os.access(path, os.R_OK)
        and os.path.getsize(path) > 0
    ):

        return True

    return False
