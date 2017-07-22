# 
# Author    : Manuel Bernal Llinares
# Project   : python-app-template
# Timestamp : 22-07-2017 7:34
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Application bootstrap script
"""

import nose
import argparse
import unittest
# Application modules
import config_manager


__DEFAULT_CONFIG_FILE = "config_default.json"

# Running mode
__run_test_mode = False
# Application Logger
__logger = None
# Command line arguments
__args = None


def get_cmdl():
    cmdl_version = '2017.07.22'
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--config_file",
                        help='Application configuration file')
    parser.add_argument('-v', '--version',
                        help='display version information',
                        action='version',
                        version=cmdl_version + ' %(prog)s ')
    args = parser.parse_args()
    return args


def app_bootstrap():
    global __run_test_mode
    global __logger
    global __args
    # Initialize configuration module
    if __args.config_file:
        config_manager.set_application_config_file(__args.config_file)
    else:
        config_manager.set_application_config_file(__DEFAULT_CONFIG_FILE)
    # Request the main logger
    __logger = config_manager.get_app_config_manager().get_logger_for(__name__)
    # TODO
    pass


def modules_bootstrap():
    # TODO
    pass


def run_unit_tests():
    __logger.debug("Running Unit Tests")
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('.')
    nose.run(suite=test_suite)


def main():
    app_bootstrap()
    modules_bootstrap()
    if __run_test_mode:
        run_unit_tests()
    else:
        # TODO - Implement what to run in normal mode
        pass

if __name__ == "__main__":
    main()
