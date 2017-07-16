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
    with open(json_file) as jf:
        return json.load(jf)
