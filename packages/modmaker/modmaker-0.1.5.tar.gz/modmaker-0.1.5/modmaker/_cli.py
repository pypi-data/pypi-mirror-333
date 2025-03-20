"""
Modmake CLI module
"""

import argparse
import signal
import sys

import requests
from importlib.metadata import version as get_distribution_version

from modmaker._cli_core import CliCore
from modmaker._common_utils import exit_with_code
from modmaker._logger import init_modmaker_cli_logger

from . import _cli_modules

LOG = init_modmaker_cli_logger(loglevel="ERROR")
BANNER = " modmaker "


class SetVerbosity(argparse.Action):
    """
    Action class for setting verbosity level in the CLI
    """

    def __call__(self, parser, namespace, values, option_string=None):
        LOG.setLevel(_get_log_level([option_string]))


NAME = "modmaker"
DESCRIPTION = "Python project skeleton generator"
GLOBAL_ARGS = [
    [
        ["-q", "--quiet"],
        {
            "action": SetVerbosity,
            "nargs": 0,
            "help": "reduce output to the minimum",
            "dest": "_quiet",
        },
    ],
    [
        ["-d", "--debug"],
        {
            "action": SetVerbosity,
            "nargs": 0,
            "help": "adds debug output and tracebacks",
            "dest": "_debug",
        },
    ],
]


def _welcome():
    """Display welcome banner"""
    LOG.info("{}\n".format(BANNER))
    try:
        # check_for_update()
        pass
    except Exception:  # pylint: disable=broad-except
        LOG.debug("Unexpected error", exc_info=True)


def _setup_logging(args, exit_func=exit_with_code):
    """Configure logging based on command line arguments
    
    Args:
        args (list): Command line arguments
        exit_func (callable): Function to call for exit
        
    Returns:
        str: Log level string
    """
    log_level = _get_log_level(args, exit_func=exit_func)
    LOG.setLevel(log_level)
    return log_level


def _print_tracebacks(log_level):
    """Determine if tracebacks should be printed based on log level
    
    Args:
        log_level (str): Current log level
        
    Returns:
        bool: True if tracebacks should be printed
    """
    return log_level == "DEBUG"


def _get_log_level(args, exit_func=exit_with_code):
    """Determine log level from command line arguments
    
    Args:
        args (list): Command line arguments
        exit_func (callable): Function to call for exit
        
    Returns:
        str: Log level string
    """
    log_level = "INFO"
    if ("-d" in args or "--debug" in args) and ("-q" in args or "--quiet" in args):
        exit_func(1, "--debug and --quiet cannot be specified simultaneously")
    if "-d" in args or "--debug" in args:
        log_level = "DEBUG"
    if "-q" in args or "--quiet" in args:
        log_level = "ERROR"
    return log_level


def _sigint_handler(signum, frame):
    """Handle SIGINT signal
    
    Args:
        signum (int): Signal number
        frame: Stack frame
    """
    LOG.debug("SIGNAL {} caught at {}".format(signum, frame))
    exit_with_code(1)


def get_pip_version(url):
    """
    Given the url to PyPI package info url returns the current live version
    
    Args:
        url (str): URL to PyPI package info
        
    Returns:
        str: Current version on PyPI
    """
    return requests.get(url, timeout=5.0).json()["info"]["version"]


def get_installed_version():
    """
    Returns the installed version of the package
    
    Returns:
        str: Installed version or message if not installed via pip
    """
    try:
        return get_distribution_version(NAME)
    except Exception:  # pylint: disable=broad-except
        return "[local source] no pip module installed"


def main(cli_core_class=CliCore, exit_func=exit_with_code):
    """
    Main entry point for the CLI
    
    Args:
        cli_core_class: CLI core class to use
        exit_func (callable): Function to call for exit
    """
    signal.signal(signal.SIGINT, _sigint_handler)
    log_level = _setup_logging(sys.argv)
    args = sys.argv[1:]
    if not args:
        args.append("-h")
    try:
        _welcome()
        version = get_installed_version()
        cli = cli_core_class(NAME, _cli_modules, DESCRIPTION, version, GLOBAL_ARGS)
        cli.parse(args)
        cli.run()

    except Exception as err:  # pylint: disable=broad-except
        LOG.error(str(err), exc_info=_print_tracebacks(log_level))
        exit_func(1)
