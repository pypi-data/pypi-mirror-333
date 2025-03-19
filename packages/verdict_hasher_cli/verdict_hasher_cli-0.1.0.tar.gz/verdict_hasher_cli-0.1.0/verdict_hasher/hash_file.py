"""
This module provides a function to compute multiple hash values for a file.
"""

import os
import hashlib
import timeit
import questionary as qy
from tqdm import tqdm


def hash_file(file_path):
    """
    Computes hash values chosen by the user for a given file and optionally writes them
    to a text file.

    Args:
        file_path (str): The path to the file to be hashed.
        Create a .txt file with the hashes at current working directory? (y/n):
            If 'y', prompts for the name of the file and writes the hash values
            to it.
        None

    Prompts:
        Create a .txt file with the hashes at current working directory? (y/n):
            If 'y', prompts for the name of the file and writes the hash
            values to it.
            If 'n', does not create a file.

    Hash Algorithms Used:
        - SHA1
        - SHA224
        - SHA256
        - SHA384
        - SHA512
        - SHA3_224
        - SHA3_256
        - SHA3_384
        - SHA3_512
        - MD5
        - BLAKE2b
        - BLAKE2s

    Example:
        hash_file('example.txt')
    """
    hash_name_list = [
        "sha1",
        "sha224",
        "sha256",
        "sha384",
        "sha512",
        "sha3_224",
        "sha3_256",
        "sha3_384",
        "sha3_512",
        "md5",
        "blake2b",
        "blake2s"
    ]
    hash_list = []
    choice_list = qy.checkbox(
        "Select hashing method(s):",
        choices=hash_name_list,
    ).ask()
    print("Starting...")
    start_time = timeit.default_timer()
    file_size = os.path.getsize(file_path)
    for c in choice_list:
        hash_list.append("hashlib." + c + "()")
    with open(file_path, 'rb') as file:
        pbar = tqdm(total=file_size, desc="Processing", unit=" Bytes")
        while True:
            chunk = file.read(1024)
            pbar.update(1024)
            if not chunk:
                pbar.close()
                break
            for h in hash_list:
                eval(h).update(chunk)
    
    choice_list_iter = iter(choice_list)
    full_choice_list = []
    for h in hash_list:
        next_choice_name = next(choice_list_iter).upper()
        full_hash = next_choice_name + ": " + eval(h).hexdigest()
        full_choice_list.append(full_hash)
        print(next_choice_name + ": " + eval(h).hexdigest())
    
    end_time = timeit.default_timer()
    print("Process completed in approximately: " + str(end_time - start_time) + " seconds")


    create = qy.confirm(
        "Create a .txt file with the hashes at current working directory? (defaults to No)",
        default=False,
        auto_enter=False
    ).ask()
    if create:
        name = input(
            "Write the name of the file (if there is a .txt file"
            " of the same name in the directory, "
            "it will likely be overwritten!): "
        )
        with open(name + ".txt", "w") as f:
            f.write("Hashes for file: " + file_path + "\n")
            for c in full_choice_list:
                f.write(c + "\n")
        print("Created file: " + f.name)
    else:
        print("File not created")
    
    return qy.press_any_key_to_continue(
        "Press any key to continue (ends program)"
    ).ask()
