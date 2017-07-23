# 
# Author    : Manuel Bernal Llinares
# Project   : python-app-template
# Timestamp : 16-07-2017 16:44
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Application general toolbox module
"""

import os
import json
import shutil
# App modules
from exceptions import ToolBoxException


def read_json(json_file="json_file_not_specified.json"):
    """
    Reads a json file and it returns its object representation, no extra checks
    are performed on the file so, in case anything happens, the exception will
    reach the caller
    :param json_file: path to the file in json format to read
    :return: an object representation of the data in the json file
    """
    with open(json_file) as jf:
        return json.load(jf)


def check_create_folders(folders):
    """
    Check if folders exist, create them otherwise
    :param folders: list of folder paths to check
    :return: no return value
    """
    for folder in folders:
        if not os.path.exists(folder):
            try:
                os.mkdir(folder)
            except Exception as e:
                raise ToolBoxException(str(e))
        else:
            if not os.path.isdir(folder):
                raise ToolBoxException("'{}' is not a folder".format(folder))


def check_create_folders_overwrite(folders):
    invalid_folders = []
    for folder in folders:
        if os.path.exists(folder):
            if not os.path.isdir(folder):
                invalid_folders.append(folder)
    if invalid_folders:
        raise ToolBoxException("The following folders ARE NOT FOLDERS - '{}'"
                               .format(invalid_folders))
    for folder in folders:
        shutil.rmtree(folder)
    check_create_folders(folders)


def gunzip_files(files):
    # TODO
    pass
