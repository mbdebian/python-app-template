# 
# Author    : Manuel Bernal Llinares
# Project   : python-app-template
# Timestamp : 29-07-2017 17:27
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Some useful helpers for dealing with RESTful web services
"""

import requests


def make_rest_request(url):
    response = requests.get(url, headers={"Content-Type": "application/json"})
    if not response.ok:
        response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    print("ERROR: This script is part of a application and it is not meant to be run in stand alone mode")
