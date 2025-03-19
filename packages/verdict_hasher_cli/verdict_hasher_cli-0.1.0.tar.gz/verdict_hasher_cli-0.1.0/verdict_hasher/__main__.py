"""
Main entry point for verdict_hasher.
"""

import sys
from file_config import file_config
from path_config import path_config
from main import main


try:
    if sys.argv[1] == "-n" or sys.argv[1] == "--name":
        file_config()
    elif sys.argv[1] == "-p" or sys.argv[1] == "--path":
        path_config()
    else:
        main()
except IndexError:
    main()
