import os

def lookup_path(path:str) -> bool:
    """
    Checks to see whether the input is a path that exists.

    Args:
        path (str): Path to be checked.

    Returns:
        bool: True if the path exists, false if it does not.
    """

    if path == None:
        return ValueError("Path must not be empty.")

    if os.path.isdir(path):
        return True
    
    else:
        return False

def lookup_file(path:str) -> bool:
    """
    Checks to see whether the input is a file that exists.

    Args:
        path (str): File to be checked.

    Returns:
        bool: True if the file exists, false if it does not.
    """

    if path == None:
        return ValueError("Path must not be empty.")

    if os.path.isfile(path):
        return True
    
    else:
        return False

