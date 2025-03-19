"""
This module provides a function to configure the path for a file and print its
hash.

Functions:
    path_config(): Prompts the user for a file path, checks if the file exists,
    and prints its hash.
"""

import os
from hash_file import hash_file


def path_config():
    """
    Prompts the user for a file path, checks if the file exists,
    and prints its hash.
    If the file does not exist, it prints "File not found".
    """
    user_file = input("Input file path (does NOT support tab completion): ")
    if os.path.isfile(user_file):
        print(hash_file(file_path=user_file))
    else:
        print("File not found")
