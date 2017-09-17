# 
# Author    : Manuel Bernal Llinares
# Project   : python-app-template
# Timestamp : 17-09-2017 6:21
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This file contains different models for the execution of subprocesses / external processes, e.g. via the command line
"""

import abc
import time
import random
import threading
import subprocess
# App imports
import config_manager
from .exceptions import ParallelRunnerException, CommandLineRunnerAsThreadException, NoMoreAliveRunnersException


class ParallelRunner(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self):
        super().__init__()
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}-{}".format(__name__, type(self).__name__, threading.current_thread().getName()))
        self._stdout = b' '
        self._stderr = b' '
        self._done = False
        self._shutdown = False

    @abc.abstractmethod
    def _run(self):
        ...

    def run(self):
        self._logger.debug("--- START ---")
        try:
            self._run()
        finally:
            self._done = True

    def cancel(self):
        self._logger.debug("--- CANCEL ---")
        self._shutdown = True
        self._stop()

