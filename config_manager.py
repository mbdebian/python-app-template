# 
# Author    : Manuel Bernal Llinares
# Project   : python-app-template
# Timestamp : 15-07-2017 8:45
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module implements configuration management for the application
"""

import os

# Application defaults - NORMAL OPERATION MODE
_folder_bin = os.path.abspath('bin')
_folder_config = os.path.abspath('config')
_folder_docs = os.path.abspath('docs')
_folder_logs = os.path.abspath('logs')
_folder_resources = os.path.abspath('resources')
_folder_run = os.path.abspath('run')

# Configuration file name
__configuration_file_name = None
