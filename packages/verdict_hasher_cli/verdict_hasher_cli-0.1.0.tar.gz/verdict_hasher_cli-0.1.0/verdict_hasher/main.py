"""
    Main module for the hash checker program.
"""
import sys
from file_config import file_config
from path_config import path_config
import questionary as qy


def main():
    """
    Main function to handle user input for file or path configuration.

    Prompts the user to input either 'Name' for file configuration, 'Path'
    for path configuration,
    or 'Exit' to exit the program. Based on the input,
    it calls the appropriate function
    or exits the program.

    Raises:
        SystemExit: If the user chooses to exit the program.
    """
    user_config = qy.select(
        "File name or path? (or exit program)",
        choices=[
            "Name",
            "Path",
            "Exit"
        ]
    ).ask()
    if user_config == "Name":
        file_config()
    elif user_config == "Path":
        path_config()
    elif user_config == "Exit":
        print("Exiting Program...")
        sys.exit(0)
    else:
        print("Input not accepted")
