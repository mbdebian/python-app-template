# 
# Author    : Manuel Bernal Llinares
# Project   : python-app-template
# Timestamp : 31-07-2017 10:41
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Download manager and its helper agents
"""

import time
import random
import threading
import subprocess


class Agent(threading.Thread):
    def __init__(self, url, dst_folder, download_attempts=32, timeout_attempts=3, download_timeout=600):
        super(Agent, self).__init__()
        self.__download_url = url
        self.__dst_folder = dst_folder
        self.__download_attempts = download_attempts
        self.__timeout_attempts = timeout_attempts
        self.__download_timeout = download_timeout
        # Compute destination file name, using the same file name as in the given URL
        self.__dst_filename = url[url.rfind("/") + 1:]
        # Prepare standard output and error output
        self.__stdout = b' '
        self.__stderr = b' '
        # Result object
        self.__result = {'msg': '', 'success': True, 'url': str(self.__download_url)}
        # Seed random module
        random.seed(time.time())


class Manager:
    pass
