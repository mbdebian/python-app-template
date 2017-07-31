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
        # We have everything we need, auto-start the thread
        self.start()

    def _build_result(self, msg, success=True):
        """
        Result object builder.

        The result object will contain anything that happened during the process of downloading a file from the given
        URL, and whether it was successful or not.
        :param msg: message to add to the final result object
        :param success: whether this extra informatoin makes the process successful or not
        :return: no value is returned
        """
        self.__result['msg'] = self.__result['msg'] + "\n" + msg
        self.__result['success'] = self.__result['success'] and success

    def __download_with_timeout(self):
        """
        This is a helper method that will download the given URL setting a timeout limit.
        :return: True if success
        :except: a subprocess.TimeoutExpired exception is raised if the download can't be completed within the given
        temporal constraints
        """
        download_command = "cd " + str(self.get_dst_folder()) + "; curl -L -O -C - " + str(self.get_download_url())
        download_subprocess = subprocess.Popen(download_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               shell=True)
        stdout = b' '
        stderr = b' '
        try:
            self._build_result("Downloading '{}' with timeout set to {} seconds"
                               .format(self.get_download_url(),
                                       self.get_download_timeout()))
            (stdout, stderr) = download_subprocess.communicate(timeout=self.get_download_timeout())
        except subprocess.TimeoutExpired as exception_download_timeout:
            self._build_result("Timeout ({} seconds) ERROR downloading '{}', STDOUT: |||> {} <|||, STDERR XXX> {} <XXX"
                               .format(self.get_download_timeout(),
                                       self.get_download_url(),
                                       stdout.decode('utf8'),
                                       stderr.decode('utf8')))
            raise
        # Let's check the result from downloading the file
        if download_subprocess.poll() is not None:
            if download_subprocess.returncode != 0:
                # ERROR
                self._build_result("ERROR downloading '{}', STDOUT: |||> {} <|||, STDERR XXX> {} <XXX"
                                   .format(self.get_download_timeout(),
                                           self.get_download_url(),
                                           stdout.decode('utf8'),
                                           stderr.decode('utf8')))
                return False
            # SUCCESS
            self._build_result("SUCCESSFUL download for '{}', STDOUT: |||> {} <|||, STDERR XXX> {} <XXX"
                               .format(self.get_download_timeout(),
                                       self.get_download_url(),
                                       stdout.decode('utf8'),
                                       stderr.decode('utf8')))
        else:
            # TODO
            # The child process is still running, and this is weird stuff because we are using a timeout parameter, we
            # should never reach this part of the code
            self._build_result("WEIRD DOWNLOAD - THE SUBPROCESS IS STILL RUNNING FOR '{}' DESPITE THE TIME OUT "
                               "PARAMETER, STDOUT: |||> {} <|||, STDERR XXX> {} <XXX"
                               .format(self.get_download_timeout(),
                                       self.get_download_url(),
                                       stdout.decode('utf8'),
                                       stderr.decode('utf8')))
            download_subprocess.kill()
            return False
        return True

    def __download_with_timeout_attempts(self):
        """
        Download the given URL given a time constraint with a limited number of attempts upon timeout errors.
        :return: True if success, False if we reached the maximum number of attempts
        """
        timeout_attempt_counter = 0
        while timeout_attempt_counter < self.get_timeout_attempts():
            self._build_result("Downloading '{}', timeout attempt #{} out of #{}"
                               .format(self.get_download_url(),
                                       timeout_attempt_counter,
                                       self.get_timeout_attempts()))
            timeout_attempt_counter += 1
            try:
                return self.__download_with_timeout()
            except subprocess.TimeoutExpired as exception_download_timeout:
                self._build_result("Download of '{}' TIMED OUT, timeout attempt #{} out of #{}"
                                   .format(self.get_download_url(),
                                           timeout_attempt_counter,
                                           self.get_timeout_attempts()))
                # wait for a random amount of time before retrying the download
                # WARNING! - MAGIC NUMBER AHEAD!!!
                time.sleep(random.randint(0, 60))
        return False

    def get_result(self):
        """
        Get the result object built by this Agent.

        This method should be called when the agent finishes its job, but not in the middle of it.
        :return: result object with information on the finished download process
        """
        return self.__result

    def get_dst_folder(self):
        return self.__dst_folder

    def get_download_timeout(self):
        return self.__download_timeout

    def get_download_url(self):
        return self.__download_url

    def get_timeout_attempts(self):
        return self.__timeout_attempts

    def get_download_attempts(self):
        return self.__download_attempts


class Manager:
    pass
