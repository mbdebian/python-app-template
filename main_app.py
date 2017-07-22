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

__DEFAULT_CONFIG_FILE = "config_default.json"

# Running mode
__run_test_mode = False
# Application Logger
__logger = None
# Command line arguments
__args = None


def get_cmdl():
    # TODO
    pass


def app_bootstrap():
    # TODO
    pass


def modules_bootstrap():
    # TODO
    pass


def run_unit_tests():
    # TODO
    pass


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
