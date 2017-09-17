# 
# Author    : Manuel Bernal Llinares
# Project   : python-app-template
# Timestamp : 17-09-2017 6:15
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Exceptions related to this parallelization module
"""

# App imports
from exceptions import AppException


class ParallelRunnerManagerException(AppException):
    def __init__(self, value):
        super().__init__(value)


class NoMoreAliveRunnersException(ParallelRunnerManagerException):
    def __init__(self, value):
        super().__init__(value)


class ParallelRunnerException(AppException):
    def __init__(self, value):
        super().__init__(value)


class CommandLineRunnerException(ParallelRunnerException):
    def __init__(self, value):
        super().__init__(value)


class CommandLineRunnerAsThreadException(CommandLineRunnerException):
    def __init__(self, value):
        super().__init__(value)


class CommandLineRunnerOnHpcException(CommandLineRunnerException):
    def __init__(self, value):
        super().__init__(value)


if __name__ == '__main__':
    print("ERROR: This script is part of an application and it is not meant to be run in stand alone mode")
