# 
# Author    : Manuel Bernal Llinares
# Project   : python-app-template
# Timestamp : 15-07-2017 9:27
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Application level exceptions
"""


class AppException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class AppConfigException(AppException):
    def __init__(self, value):
        super().__init__(value)


class ConfigManagerException(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)


class ToolBoxException(AppException):
    def __init__(self, value):
        super(ToolBoxException, self).__init__(value)


if __name__ == '__main__':
    print("ERROR: This script is part of a application and it is not meant to be run in stand alone mode")
