# 
# Author    : Manuel Bernal Llinares
# Project   : python-app-template
# Timestamp : 15-07-2017 8:45
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module implements configuration management for the application
"""

import os
# App imports
from toolbox import general
from exceptions import AppConfigException, ConfigManagerException

# Application defaults - NORMAL OPERATION MODE
_folder_bin = os.path.abspath('bin')
_folder_config = os.path.abspath('config')
_folder_docs = os.path.abspath('docs')
_folder_logs = os.path.abspath('logs')
_folder_resources = os.path.abspath('resources')
_folder_run = os.path.abspath('run')

# Configuration file name
__configuration_file_name = None

# Logging defaults
_logger_formatters = {
    "DEBUG": "%(asctime)s [%(levelname)7s][%(name)28s][%(module)18s, %(lineno)4s] %(message)s",
    "INFO": "%(asctime)s [%(levelname)7s][%(name)28s] %(message)s"
}
_log_level = 'DEBUG'


def set_application_config_file(configuration_file):
    """
    This method sets the application wide configuration file that will be used
    :param configuration_file: config file name if the file is in the default configuration path or path to the
    configuration file if it is not.
    :return: no return value
    :exception: ConfigException is raised if there already is a configuration file set
    """
    global __configuration_file_name
    if __configuration_file_name is not None:
        raise AppConfigException(
            "Configuration file can't be changed once an initial configuartion file has been provided")
    __configuration_file_name = configuration_file


# Configuration Singleton
__app_config_manager = None


def get_app_config_manager():
    pass


def read_config_from_file(configuration_file):
    """
    Given a file name or absolute path, read its configuration information in json format and return its object
    representation
    :param configuration_file: file name or absolute path for the file that contains the configuration information
    :return: an object representation of the json formatted configuration information read from the file
    """
    config_file_path = configuration_file
    if not os.path.isabs(config_file_path):
        config_file_path = os.path.join(_folder_config, configuration_file)
    try:
        return general.read_json(config_file_path)
    except Exception as e:
        msg = "Config file {} could not be read, because {}".format(config_file_path, str(e))
        raise AppConfigException(msg)


class ConfigurationManager:
    """
    This class is a helper class for those submodules having to manage configuration files themselves, that are specific
    to them
    """

    def __init__(self, configuration_object, configuration_file):
        self.__configuration_object = configuration_object
        self.__configuration_file = configuration_file

    def _get_value_for_key(self, key):
        if key in self.__configuration_object:
            return self.__configuration_object[key]
        else:
            msg = "MISSING configuration key '{}' in configuration file '{}'".format(key, self.__configuration_file)
            raise ConfigManagerException(msg)

    def _get_value_for_key_with_default(self, key, default):
        if key in self.__configuration_object:
            return self.__configuration_object[key]
        else:
            return default

    def _get_configuration_object(self):
        return self.__configuration_object

    def _get_configuration_file(self):
        return self.__configuration_file


class AppConfigManager(ConfigurationManager):
    """
    Application wide Configuration Manager
    """

    # TODO - Constructor

    def _get_logger(self):
        # Get own logger
        return self.__logger

    def _get_log_handlers(self):
        return self.__log_handlers

    def get_folder_bin(self):
        # 'Bin' folder cannot be changed in this version of the template
        return _folder_bin

    def get_folder_config(self):
        # Configuration folder cannot be changed in this version of the template
        return _folder_config

    def get_folder_logs(self):
        # Configuration for logging folder cannot be changed in this version of the template
        return _folder_logs

    def get_folder_resources(self):
        # Configuration for resources folder cannot be changed in this version of the template
        return _folder_resources

    def get_folder_run(self):
        # Configuration for 'run' folder cannot be changed in this version of the template
        return _folder_run

    def get_session_working_dir(self):
        return self.__session_working_dir

    def get_logger_for(self, name):
        """
        Create a logger on demand
        :param name: name to be used in the logger
        :return: a new logger on that name
        """
        self._get_logger().debug("Creating logger with name {}".format(name))
        lg = logging.getLogger(name)
        for handler in self._get_log_handlers():
            lg.addHandler(handler)
        lg.setLevel(_log_level)
        return lg

    def get_session_id(self):
        return self.__session_id
