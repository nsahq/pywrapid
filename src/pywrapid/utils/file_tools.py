#!/usr/bin/python3
"""
Collection of file helper functions
"""
import logging
import os
import re
from typing import Any

log = logging.getLogger(__name__)
# flake8: noqa: C901


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


def is_file_writable(path: str) -> bool:
    """Checks a file in a given path to make sure it:
        - exists
        - is a file
        - is writable

    Args:
        path (str): Path to configuration file.

    Returns:
        bool: True/False.
    """
    if os.path.exists(path) and os.path.isfile(path) and os.access(path, os.W_OK):
        return True

    return False


def is_directory_readable(path: str) -> bool:
    """Checks a directory in a given path to make sure it:
        - exists
        - is a directory
        - is readable

    Args:
        path (str): Path to configuration file.

    Returns:
        bool: True/False.
    """
    if os.path.exists(path) and os.path.isdir(path) and os.access(path, os.R_OK):
        return True

    return False


def is_directory_writable(path: str) -> bool:
    """Checks a directory in a given path to make sure it:
        - exists
        - is a directory
        - is writable

    Args:
        path (str): Path to configuration file.

    Returns:
        bool: True/False.
    """
    if os.path.exists(path) and os.path.isdir(path) and os.access(path, os.W_OK):
        return True

    return False


def get_metadata(path: str) -> dict:
    """Internal function to get filesystem object metadata

    Args:
        path (str): Path to fileystem object.

    Returns:
        dict:   Filesystem object metadata.
                name (str),
                path (str),
                size (int) Files only,
                access time (int or float),
                crete time (int or float),
                modify time (int or float),
                group (int),
                owner (int),
                permissions (oct),
                inode (int),
                mount_point (bool) directory only,
                symlink (symlink only),
                type (str) file|directory|symlink,
    """
    try:
        stat = os.stat(path)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Unable to get metadata for {path}") from error
    # except OSError as error:
    #     raise OSError(f"Error getting metadata for {path}") from error

    metadata = {
        "name": os.path.basename(path),
        "path": os.path.abspath(path),
        "size": stat.st_size,
        "access_time": stat.st_atime,
        "create_time": stat.st_ctime,
        "modify_time": stat.st_mtime,
        "group": stat.st_gid,
        "owner": stat.st_uid,
        "permissions": stat.st_mode,
        "inode": stat.st_ino,
    }

    if os.path.isdir(path):
        metadata["type"] = "directory"
        metadata.pop("size")
        metadata["mount_point"] = os.path.ismount(path)
    elif os.path.isfile(path):
        metadata["type"] = "file"

    if os.path.islink(path):
        metadata["type"] = "symlink"
        metadata["symlink"] = os.path.realpath(path)

    return metadata


def find_directory_content(  # pylint: disable=R0912,R0914
    path: str, depth: int = 0, **options: Any
) -> list[dict]:
    """Get directory content and allow os walk.
    Includes sub levels of user defined depth with metadata and item names as list of dict return.

    Args:
        path (str): Path to configuration file.
        depth (int, optional): Depth to walk. Defaults to 0/unlimited.

    Options:
        exclude_files (bool, optional): Exclude files from return. Defaults to False.
        exclude_directories (bool, optional): Exclude directories from return. Defaults to False.
        exclude_symlinks (bool, optional): Exclude symlinks from return. Defaults to False.
        exclude_pattern (str, optional): Pattern to exclude. Defaults to "".
        follow_symlinks (bool, optional): Follow symlinks. Defaults to False.

    Returns:
        list[dict]: List of dict with metadata and item names
                    type (file, directory, symlink),
                    name,
                    path,
                    size,
                    access time,
                    crete time,
                    modify time,
                    group,
                    owner,
                    permissions,
                    inode
    """
    # Handle options
    follow_symlinks = options.get("follow_symlinks", False)
    exclude_directories = options.get("exclude_directories", False)
    exclude_files = options.get("exclude_files", False)
    exclude_symlinks = options.get("exclude_symlinks", False)
    exclude_patterns: list[str] = options.get("exclude_patterns", [])

    results = []
    # Abort if base path is not readable
    if not is_directory_readable(path):
        raise OSError(f"Path {path} is not readable")
    path = os.path.normpath(path)

    base_depth = path.count(os.path.sep)

    # Walk the directory tree and process items
    for root, dirs, files in os.walk(
        path,
        topdown=True,
        followlinks=follow_symlinks,
    ):
        cur_depth = root.count(os.path.sep)
        if depth and base_depth + depth <= cur_depth:
            del dirs[:]
            del files[:]
            # continue

        sym_dirs = [d for d in dirs if os.path.islink(os.path.join(root, d))]
        sym_files = [f for f in files if os.path.islink(os.path.join(root, f))]

        if exclude_symlinks:
            if sym_dirs:
                log.debug("Excluding %s symlinked directories", len(sym_dirs))
                dirs[:] = [d for d in dirs if d not in sym_dirs]

            if sym_files:
                log.debug("Excluding %s symlinked files", len(sym_files))
                files[:] = [f for f in files if f not in sym_files]

        if exclude_patterns:
            for exclude_pattern in exclude_patterns:
                dir_count = len(dirs)
                file_count = len(files)
                dirs[:] = [d for d in dirs if not re.findall(exclude_pattern, d)]
                files[:] = [f for f in files if not re.findall(exclude_pattern, f)]
                log.debug(
                    "Excluding %s files and %s directories due to pattern matching: %s",
                    file_count - len(files),
                    dir_count - len(dirs),
                    exclude_pattern,
                )

        if not exclude_directories and dirs:
            for directory in dirs:
                results.append(get_metadata(os.path.join(root, directory)))
        elif exclude_directories and not exclude_symlinks and sym_dirs:
            for directory in sym_dirs:
                results.append(get_metadata(os.path.join(root, directory)))

        if not exclude_files and files:
            for file in files:
                results.append(get_metadata(os.path.join(root, file)))
        elif exclude_files and not exclude_symlinks and sym_files:
            for file in sym_files:
                results.append(get_metadata(os.path.join(root, file)))

    return results
