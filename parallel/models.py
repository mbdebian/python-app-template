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


# Abstract Factories
class CommandLineRunnerFactory:
    @staticmethod
    def get_command_line_runner():
        # This is the automatic selector between command line runners
        # TODO - This Factory is creating only local runners in the first iteration
        return CommandLineRunnerAsThread()

    # Having the following two methods allows the application to use a multithreaded command line runner in an HPC
    # system, e.g. in those situations where you don't want your command line runners to queue more jobs in an
    # sHPC environment
    @staticmethod
    def get_multithread_command_line_runner():
        return CommandLineRunnerAsThread()

    @staticmethod
    def get_hpc_command_line_runner():
        return CommandLineRunnerOnHpc()


class ParallelRunnerManagerFactory:
    @staticmethod
    def get_parallel_runner_manager():
        # TODO - This factory is creating only one kind of Parallel Runner Manager, more complex ones to come ...
        return ParallelRunnerManager()


# Parallel Runner Managers
class ParallelRunnerManager:
    """
    This class models a manager for parallel runners, that will handle common operations on them like starting the
    runners, waiting for them to finish or getting the next one that finished.
    """
    # TODO - Include an 'auto_start' flag to start runners as they are added to the manager
    def __init__(self):
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))
        self.__runners = set()
        self.__alive_runners = set()
        self.__finished_runners = set()

    def add_runners(self, runners):
        self.__runners.union(set(runners))

    def add_runner(self, runner):
        self.__runners.add(runner)

    def start_runners(self):
        self._logger.debug("Starting #{} Runners".format(len(self.__runners)))
        for runner in self.__runners:
            runner.start()
            self.__alive_runners.add(runner)
        self._logger.debug("Runners started, clearing out the runners container")
        self.__runners.clear()

    def get_next_finished_runner(self):
        if not self.__alive_runners:
            raise NoMoreAliveRunnersException("No more runners left! They've all finished")
        runner_found = None
        counter = 1
        while True:
            self._logger.debug("Searching for the next finished runner among #{} runners, ROUND #{}"
                               .format(len(self.__alive_runners),
                                       counter))
            for runner in self.__alive_runners:
                if runner.is_done():
                    runner_found = runner
                    break
            if runner_found:
                self.__alive_runners.remove(runner_found)
                self.__finished_runners.add(runner_found)
                break
            # WARNING! - MAGIC NUMBER AHEAD!!!
            # We haven't found any runner on this round, let's wait a random amount of time before we try again
            time.sleep(random.randint(0, 10))
            counter += 1
        return runner_found

    def wait_all(self):
        self._logger.debug("Waiting for all #{} runners to finish".format(len(self.__alive_runners)))
        try:
            while True:
                self.get_next_finished_runner()
        except NoMoreAliveRunnersException as e:
            self._logger.debug("All runners are (should be) finished")

    def get_not_started_runners(self):
        return set(self.__runners)

    def get_alive_runners(self):
        return set(self.__alive_runners)

    def get_finished_runners(self):
        return set(self.__finished_runners)


# Parallel Runners
class ParallelRunner(threading.Thread, metaclass=abc.ABCMeta):
    # TODO - Refactor This, as responsibilities are a little bit mixed up
    def __init__(self):
        super().__init__()
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}-{}".format(__name__, type(self).__name__, threading.current_thread().getName()))
        # Flags
        self._done = False
        self._error = False
        self._shutdown = False
        # Return information (this could be an entity on its own in the next iteration)
        self._error_messages = []

    @abc.abstractmethod
    def _run(self):
        ...

    def run(self):
        self._logger.debug("--- START ---")
        try:
            self._run()
        except ParallelRunnerException as e:
            # This code is running on a separated thread, so this class, as top level 'client', must log the error for
            # the application
            error_message = "Parallel Runner failed ---> '{}'".format(e.value)
            self._error_messages.append(error_message)
            self._logger.error(error_message)
            self._error = True
        finally:
            self._done = True

    def cancel(self):
        self._logger.debug("--- CANCEL ---")
        self._shutdown = True
        self._stop()

    def wait(self):
        self._logger.debug("--- WAIT ---")
        self.join()

    def is_done(self):
        return self._done

    def is_error(self):
        return self._error


# Execution of commands
class CommandLineRunner(ParallelRunner):
    def __init__(self):
        super().__init__()
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))
        self._stdout = b' '
        self._stderr = b' '
        self.command = None
        self.command_success = False
        self.command_return_code = 0
        self.timeout = None
        self.current_working_directory = None

    def get_stdout(self):
        # Never give it back until the runner is done with whatever it is doing
        if not self._done:
            raise ParallelRunnerException("Runner is NOT DONE doing its job, thus 'stdout' is NOT AVAILABLE")
        return self._stdout

    def get_stderr(self):
        # Never give it back until the runner is done with whatever it is doing
        if not self._done:
            raise ParallelRunnerException("Runner is NOT DONE doing its job, thus 'stderr' is NOT AVAILABLE")
        return self._stderr


class CommandLineRunnerAsThread(CommandLineRunner):
    def __init__(self):
        super().__init__()
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}-{}".format(__name__, type(self).__name__, threading.current_thread().getName()))

    def _run(self):
        self._logger.debug("Preparing for running command '{}', "
                           "current working directory at '{}', "
                           "timeout '{}s'".format(self.command,
                                                  self.current_working_directory,
                                                  self.timeout))
        command_subprocess = subprocess.Popen(self.command,
                                              cwd=self.current_working_directory,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE,
                                              shell=True)
        self._logger.debug("Communicating with subprocess for command '{}', "
                           "current working directory at '{}', "
                           "timeout '{}s'".format(self.command,
                                                  self.current_working_directory,
                                                  self.timeout))
        try:
            self._stdout, self._stderr = command_subprocess.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired as e:
            command_subprocess.kill()
            raise CommandLineRunnerAsThreadException("Communicating with subprocess for command '{}', "
                                                     "current working directory at '{}', "
                                                     "timeout '{}s'".format(self.command,
                                                                            self.current_working_directory,
                                                                            self.timeout)) from e
        self._logger.debug("Polling command '{}', "
                           "current working directory at '{}', "
                           "timeout '{}s'".format(self.command,
                                                  self.current_working_directory,
                                                  self.timeout))
        if command_subprocess.poll() and (command_subprocess.returncode != 0):
            self.command_return_code = command_subprocess.returncode
            raise CommandLineRunnerAsThreadException("ERROR - Return Code '{}' for command '{}', "
                                                     "current working directory at '{}', "
                                                     "timeout '{}s'".format(command_subprocess.returncode,
                                                                            self.command,
                                                                            self.current_working_directory,
                                                                            self.timeout))
        # I don't think I really need this flag over here, as any other situation would throw an exception but, it looks
        # good and, keep into account that whatever you do with a possible exception is independent than whatever you
        # can express by the combination of flags '_done' and 'command_success'. This allows you to react by capturing
        # the exception (that also provides the return code for the command) but still keep the information that the
        # process finished Ok, but the command failed, and you also have the stdout and stderr content for further
        # analysis
        self.command_success = True


class CommandLineRunnerOnHpc(CommandLineRunner):
    def __init__(self):
        super().__init__()
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}-{}".format(__name__, type(self).__name__, threading.current_thread().getName()))

    def _run(self):
        pass


if __name__ == '__main__':
    print("ERROR: This script is part of an application and it is not meant to be run in stand alone mode")
