import os

def super_touch(_file):
    """
    Create file and all parent directories.

    Copied from `bshlib` library.

    Parameters
    -----
    _file : `Path`
        File.
    """
    os.makedirs(_file.parent, exist_ok=True)
    os.mknod(_file)
