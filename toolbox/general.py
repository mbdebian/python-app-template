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

import json


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
    # TODO
    pass


def check_create_folders_overwrite(folders):
    # TODO
    pass


def gunzip_files(files):
    # TODO
    pass