# 
# Author    : Manuel Bernal Llinares
# Project   : python-app-template
# Timestamp : 31-07-2017 11:12
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Unit Tests for the download manager module
"""

import unittest
# App imports
import config_manager
from download_manager.manager import Manager as DownloadManager


class TestDownloadManager(unittest.TestCase):
    __logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def test_success_on_sample_files_download(self):
        urls = ['http://ipv4.download.thinkbroadband.com/5MB.zip',
                'http://ipv4.download.thinkbroadband.com/10MB.zip',
                'http://ipv4.download.thinkbroadband.com/20MB.zip',
                'http://ipv4.download.thinkbroadband.com/50MB.zip']
        destination_folder = config_manager.get_app_config_manager().get_session_working_dir()
        # Log the test environment
        self.__logger.info("Sample file URLs to download: {}".format(",".join(urls)))
        self.__logger.info("Destination folder for the downloads, '{}'".format(destination_folder))
        # Get the download manager and start the downloads
        download_manager = DownloadManager(urls, destination_folder, self.__logger)
        download_manager.start_downloads()
        download_manager.wait_all()
        self.assertTrue(download_manager.is_success(), "Files downloaded successfully")


if __name__ == '__main__':
    print("ERROR: This script is part of a application and it is not meant to be run in stand alone mode")
