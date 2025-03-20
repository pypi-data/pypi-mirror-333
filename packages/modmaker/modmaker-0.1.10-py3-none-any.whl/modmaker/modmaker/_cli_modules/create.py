"""
Create a new Python project skeleton
"""

import logging
import os
import sys
import shutil
from pathlib import Path

from modmaker._common_utils import ensure_directory, copy_directory_contents, exit_with_code

LOG = logging.getLogger(__name__)


class Create:
    """
    Create a new Python project skeleton with CLI functionality
    """
    
    CLINAME = "create"

    def __init__(self):
        self.description = "Create a new Python project skeleton"
        LOG.info("Initializing project creation...")

    def project(self, name: str):
        """
        Create a new project
        
        :param name: The name of the project to create
        """
        LOG.info(f"Creating new project: {name}")
        
        # Create project directory
        current_dir = os.getcwd()
        project_dir = os.path.join(current_dir, name)
        
        if os.path.exists(project_dir):
            LOG.error(f"Directory {project_dir} already exists")
            exit_with_code(1, f"Directory {project_dir} already exists")
        
        # Create project structure
        ensure_directory(project_dir)
        
        # Get template directory
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "cli")
        
        if not os.path.exists(template_dir):
            LOG.error(f"Template directory not found: {template_dir}")
            exit_with_code(1, f"Template directory not found: {template_dir}")
        
        # Copy basic structure
        success = self._copy_template(template_dir, project_dir, name)
        if not success:
            exit_with_code(1, "Failed to create project structure")
            
        # Create CLI structure
        success = self._create_cli_structure(project_dir, name)
        if not success:
            exit_with_code(1, "Failed to create CLI structure")
            
        LOG.info(f"Project {name} created successfully")
        print(f"Project {name} created successfully")
        return True
        
    def _copy_template(self, template_dir, project_dir, project_name):
        """
        Copy template files to the project directory
        
        Args:
            template_dir (str): Source template directory
            project_dir (str): Destination project directory
            project_name (str): Name of the project
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Handle special files/dirs first
            # Copy and rename project directory template
            src_project_dir = os.path.join(template_dir, "{{PROJECT_NAME}}")
            dst_project_dir = os.path.join(project_dir, project_name)
            
            if os.path.exists(src_project_dir):
                os.makedirs(dst_project_dir, exist_ok=True)
                copy_directory_contents(src_project_dir, dst_project_dir)
            
            # Copy other files (excluding the project dir template)
            for item in os.listdir(template_dir):
                if item == "{{PROJECT_NAME}}":
                    continue
                    
                src_item = os.path.join(template_dir, item)
                dst_item = os.path.join(project_dir, item)
                
                if os.path.isdir(src_item):
                    shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_item, dst_item)
            
            # Replace template variables in all files
            self._replace_variables(project_dir, {
                "{{PROJECT_NAME}}": project_name,
                "{{AUTHOR}}": "Your Name",
                "{{EMAIL}}": "your.email@example.com",
                "{{LICENSE}}": "Apache-2.0",
                "{{PYTHON_VERSION}}": "3.8"
            })
            
            return True
        except Exception as e:
            LOG.error(f"Error copying template: {str(e)}")
            return False
            
    def _create_license_file(self, project_dir):
        """
        Create a license file with Apache 2.0 license
        
        Args:
            project_dir (str): Project directory
        """
        pass  # License file is now handled through the template system
    
    def _create_cli_structure(self, project_dir, project_name):
        """
        Create CLI structure files
        
        Args:
            project_dir (str): Project directory
            project_name (str): Name of the project
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create license file
            self._create_license_file(project_dir)
            
            # Create _cli_modules directory
            cli_modules_dir = os.path.join(project_dir, project_name, "_cli_modules")
            ensure_directory(cli_modules_dir)
            
            # Create CLI files
            self._create_file(project_dir, project_name, "_cli.py", self._get_cli_content(project_name))
            self._create_file(project_dir, project_name, "_cli_core.py", self._get_cli_core_content(project_name))
            self._create_file(project_dir, project_name, "_common_utils.py", self._get_common_utils_content(project_name))
            self._create_file(project_dir, project_name, "_logger.py", self._get_logger_content(project_name))
            
            # Create _cli_modules/__init__.py
            self._create_file(project_dir, project_name, "_cli_modules/__init__.py", self._get_cli_modules_init_content(project_name))
            
            # Create _cli_modules/option.py
            self._create_file(project_dir, project_name, "_cli_modules/option.py", self._get_cli_modules_option_content(project_name))
            
            return True
        except Exception as e:
            LOG.error(f"Error creating CLI structure: {str(e)}")
            return False
            
    def _create_file(self, project_dir, project_name, relative_path, content):
        """
        Create a file with the given content
        
        Args:
            project_dir (str): Project directory
            project_name (str): Name of the project
            relative_path (str): Path relative to the project module
            content (str): File content
        """
        file_path = os.path.join(project_dir, project_name, relative_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(content)
            
    def _replace_variables(self, directory, variables):
        """
        Replace template variables in all files in the directory
        
        Args:
            directory (str): Directory to process
            variables (dict): Variables to replace
        """
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.py', '.md', '.toml', '.txt')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                            
                        for var, value in variables.items():
                            content = content.replace(var, value)
                            
                        with open(file_path, 'w') as f:
                            f.write(content)
                    except Exception as e:
                        LOG.error(f"Error processing file {file_path}: {str(e)}")
                        
    def _get_cli_content(self, project_name):
        """
        Get the content for _cli.py
        """
        return f'''"""
{project_name} CLI module
"""

import argparse
import signal
import sys

import requests
from importlib.metadata import version as get_distribution_version

from {project_name}._cli_core import CliCore
from {project_name}._common_utils import exit_with_code
from {project_name}._logger import init_{project_name}_cli_logger

from . import _cli_modules

LOG = init_{project_name}_cli_logger(loglevel="ERROR")
BANNER = " {project_name} "


class SetVerbosity(argparse.Action):
    """
    Action class for setting verbosity level in the CLI
    """

    def __call__(self, parser, namespace, values, option_string=None):
        LOG.setLevel(_get_log_level([option_string]))


NAME = "{project_name}"
DESCRIPTION = "Python project skeleton generator"
GLOBAL_ARGS = [
    [
        ["-q", "--quiet"],
        {{
            "action": SetVerbosity,
            "nargs": 0,
            "help": "reduce output to the minimum",
            "dest": "_quiet",
        }},
    ],
    [
        ["-d", "--debug"],
        {{
            "action": SetVerbosity,
            "nargs": 0,
            "help": "adds debug output and tracebacks",
            "dest": "_debug",
        }},
    ],
]


def _welcome():
    """Display welcome banner"""
    LOG.info("{{}}\\n".format(BANNER))
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
    LOG.debug("SIGNAL {{}} caught at {{}}".format(signum, frame))
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
'''

    def _get_cli_core_content(self, project_name):
        """
        Get the content for _cli_core.py
        """
        return f'''"""
CLI Core module for {project_name}

This module provides the core CLI functionality, including argument parsing
and command execution.
"""

import argparse
import importlib
import inspect
import logging
import sys
import types

LOG = logging.getLogger(__name__)


class CliCore:
    """Core CLI class that handles command parsing and execution"""
    
    USAGE = "{{prog}}{{global_opts}}{{command}}{{command_opts}}{{subcommand}}{{subcommand_opts}}"

    def __init__(self, prog_name, module_package, description, version=None, args=None):
        """Initialize the CLI core.
        
        Args:
            prog_name (str): The program name
            module_package: The package containing command modules
            description (str): Program description
            version (str, optional): Version string. Defaults to None.
            args (list, optional): List of global args. Defaults to None.
        """
        self.name = prog_name
        self.module_package = module_package
        self._modules = self._get_plugin_modules()
        self.args = {{"global": args if args is not None else [], "commands": {{}}}}
        self._build_args()
        self.command_parser = None
        self.subcommand_parsers = {{}}
        self.parser = self._build_parser(description, version)
        self.parsed_args = []

    def _build_args(self):
        """Build command and subcommand arguments"""
        for name, module in self._modules.items():
            params = self._get_params(module)
            self.args["commands"][name] = {{"args": params, "subcommands": {{}}}}
            for method_name, method_function in self._get_class_methods(module):
                if not method_name.startswith("_"):
                    params = self._get_params(method_function)
                    self.args["commands"][name]["subcommands"][method_name] = params

    @staticmethod
    def _get_class_methods(module):
        """Get all non-private methods of a class.
        
        Args:
            module: Module to inspect
            
        Returns:
            list: List of (method_name, method_function) tuples
        """
        methods = inspect.getmembers(module, predicate=inspect.isfunction)
        return [method for method in methods if not method[0].startswith("_")]

    @staticmethod
    def _get_params(item):
        """Extract parameters from a function or class.
        
        Args:
            item: Function or class to inspect
            
        Returns:
            list: List of parameter definitions
        """
        params = []
        for param in inspect.signature(item).parameters.values():
            if param.name == "self" or param.name.startswith("_"):
                continue
            required = param.default == param.empty
            default = param.default if not required else None
            val_type = param.annotation if param.annotation in [str, int, bool] else str
            action = "store_true" if val_type == bool else "store"
            param_help = CliCore._get_param_help(item, param.name)
            name = param.name.lower()
            kwargs = {{"action": action, "help": param_help}}
            if not required:
                name = name.replace("_", "-")
                kwargs.update(
                    {{"required": required, "default": default, "dest": param.name}}
                )
            if action == "store":
                kwargs.update({{"type": val_type}})
            params.append(
                [[name] if required else [f"-{{name[0]}}", f"--{{name}}"], kwargs]
            )
        return params

    @staticmethod
    def _get_param_help(item, param):
        """Extract help text for a parameter from docstring.
        
        Args:
            item: Function or class
            param (str): Parameter name
            
        Returns:
            str: Help text for the parameter
        """
        help_str = ""
        docstring = (
            item.__doc__
            if isinstance(item, types.FunctionType)
            else item.__init__.__doc__
        )
        if docstring is None:
            return help_str
        for line in docstring.split("\\n"):
            if line.strip().startswith(f":param {{param}}:"):
                help_str = line.strip()[len(f":param {{param}}:") :].strip()
                break
        return help_str

    @staticmethod
    def _get_help(item):
        """Extract general help text from docstring.
        
        Args:
            item: Function or class with docstring
            
        Returns:
            str: Help text extracted from docstring
        """
        help_str = ""
        if item.__doc__ is None:
            return help_str
        for line in item.__doc__.split("\\n"):
            if not line.strip().startswith(":"):
                help_str += line.strip()
        return help_str.strip()

    def _get_command_help(self, commands):
        """Build help text for a set of commands.
        
        Args:
            commands (dict): Dictionary of command modules
            
        Returns:
            str: Formatted help text
        """
        help_str = ""
        for name, mod in commands.items():
            mod_help = self._get_help(mod)
            if not mod_help:
                help_str += f"{{name}}\\n"
            else:
                help_str += f"{{name}} - {{mod_help}}\\n"
        return help_str.strip()

    def _add_subparser(self, usage, description, mod, parser, args):
        """Add a subparser for a command or subcommand.
        
        Args:
            usage (str): Usage text
            description (str): Command description
            mod (str): Module/command name
            parser: Parent parser
            args (list): Arguments for this parser
            
        Returns:
            argparse.Parser: The created subparser
        """
        sub_parser = parser.add_parser(
            mod,
            usage=usage,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        self._add_arguments(args, sub_parser)
        return sub_parser

    @staticmethod
    def _add_arguments(input_args, parser):
        """Add arguments to a parser.
        
        Args:
            input_args (list): List of argument definitions
            parser: Parser to add arguments to
        """
        for args, kwargs in input_args:
            parser.add_argument(*args, **kwargs)

    @staticmethod
    def _add_sub(parser, **kwargs):
        """Add a subparser with compatibility for different Python versions.
        
        Args:
            parser: Parent parser
            **kwargs: Keyword arguments for add_subparsers
            
        Returns:
            subparser: Created subparser
        """
        # Python 3.7+ handles required directly
        if sys.version_info.minor >= 7 or "required" not in kwargs:
            return parser.add_subparsers(**kwargs)
        required = kwargs["required"]
        kwargs.pop("required")
        sub = parser.add_subparsers(**kwargs)
        sub.required = required
        return sub

    def _build_parser(self, description, version):
        """Build the main argument parser with all commands and subcommands.
        
        Args:
            description (str): Program description
            version (str): Version string
            
        Returns:
            argparse.ArgumentParser: Configured parser
        """
        parser = argparse.ArgumentParser(
            description=description,
            usage=self._build_usage(),
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        if version:
            parser.add_argument("-v", "--version", action="version", version=version)
        # Add global arguments
        self._add_arguments(self.args["global"], parser)

        description = self._get_command_help(self._modules)
        command_parser = self._add_sub(
            parser=parser,
            title="commands",
            description=description,
            required=True,
            metavar="",
            dest="_command",
        )
        self.command_parser = command_parser
        for mod in self._modules:
            usage = self._build_usage({{"command": mod}})
            description = self._get_help(self._modules[mod])
            mod_parser = self._add_subparser(
                usage,
                description,
                mod,
                command_parser,
                self.args["commands"][mod]["args"],
            )
            self.subcommand_parsers[mod] = mod_parser
            # add subcommand parser if subcommands exist
            subcommands = self.args["commands"][mod]["subcommands"]
            if subcommands:
                class_methods = {{
                    m[0]: m[1] for m in self._get_class_methods(self._modules[mod])
                }}
                description = self._get_command_help(class_methods)
                subcommand_parser = self._add_sub(
                    parser=mod_parser,
                    title="subcommands",
                    description=description,
                    required=True,
                    metavar="",
                    dest="_subcommand",
                )
                for subcommand_name, subcommand_args in subcommands.items():
                    usage = self._build_usage({{"subcommand": subcommand_name}})
                    description = self._get_help(class_methods[subcommand_name])
                    self._add_subparser(
                        usage,
                        description,
                        subcommand_name,
                        subcommand_parser,
                        subcommand_args,
                    )
        return parser

    def _build_usage(self, args=None):
        """Build usage string for help text.
        
        Args:
            args (dict, optional): Arguments to include in usage. Defaults to None.
            
        Returns:
            str: Formatted usage string
        """
        args = args if args is not None else {{}}
        args["prog"] = self.name
        if "command" not in args:
            args["command"] = "<command>"
        if "subcommand" not in args:
            args["subcommand"] = "[subcommand]"
        if "global_opts" not in args:
            args["global_opts"] = "[args]"
        if "command_opts" not in args:
            args["command_opts"] = "[args]"
        if "subcommand_opts" not in args:
            args["subcommand_opts"] = "[args]"
        for key, val in args.items():
            if val and not val.endswith(" "):
                args[key] = f"{{val}} "
        return self.USAGE.format(**args)

    def _get_plugin_modules(self):
        """Get all plugin modules from the module package.
        
        Returns:
            dict: Dictionary of module name -> module
        """
        # pylint: disable=invalid-name
        members = inspect.getmembers(self.module_package, predicate=inspect.isclass)
        member_name_class = []
        for name, cls in members:
            if hasattr(cls, "CLINAME"):
                name = cls.CLINAME
            member_name_class.append((name, cls))
        return {{name.lower(): cls for name, cls in member_name_class}}

    @staticmethod
    def _import_plugin_module(class_name, module_name):
        """Import a plugin module by name.
        
        Args:
            class_name (str): Class name to import
            module_name (str): Module name
            
        Returns:
            module: The imported module
        """
        return getattr(importlib.import_module(module_name), class_name)

    def parse(self, args=None):
        """Parse command line arguments.
        
        Args:
            args (list, optional): Arguments to parse. Defaults to None.
            
        Returns:
            argparse.Namespace: Parsed arguments
        """
        if not args:
            args = []
        self.parsed_args = self.parser.parse_args(args)
        return self.parsed_args

    def run(self):
        """Run the command specified by the parsed arguments.
        
        Returns:
            Any: Result of command execution
        """
        args = self.parsed_args.__dict__
        command = self._modules[args["_command"]]
        subcommand = ""
        if "_subcommand" in args:
            subcommand = args["_subcommand"]
        args = {{k: v for k, v in args.items() if not k.startswith("_")}}
        if not subcommand:
            return command(**args)
        return getattr(command(), subcommand)(**args)
'''

    def _get_common_utils_content(self, project_name):
        """
        Get the content for _common_utils.py
        """
        return f'''"""
Common utility functions for {project_name}
"""

import logging
import sys
import os
import shutil
from pathlib import Path

LOG = logging.getLogger(__name__)


def exit_with_code(code, msg=""):
    """Exit the application with a specific code and optional message
    
    Args:
        code (int): Exit code
        msg (str, optional): Optional error message. Defaults to "".
    """
    if msg:
        LOG.error(msg)
    sys.exit(code)


def ensure_directory(path):
    """Ensure a directory exists, creating it if necessary
    
    Args:
        path (str): Directory path to create
        
    Returns:
        bool: True if directory exists or was created, False otherwise
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        LOG.error(f"Failed to create directory {{path}}: {{str(e)}}")
        return False


def copy_directory_contents(src, dest):
    """Copy all contents from source directory to destination
    
    Args:
        src (str): Source directory path
        dest (str): Destination directory path
        
    Returns:
        bool: True if copy was successful, False otherwise
    """
    try:
        if not os.path.exists(dest):
            os.makedirs(dest)
            
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dest_item = os.path.join(dest, item)
            
            if os.path.isdir(src_item):
                shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(src_item, dest_item)
        return True
    except Exception as e:
        LOG.error(f"Failed to copy directory contents: {{str(e)}}")
        return False
'''

    def _get_logger_content(self, project_name):
        """
        Get the content for _logger.py
        """
        return f'''"""
Logging utilities for {project_name}
"""

import logging


class PrintMsg:
    header = "\\x1b[1;41;0m"
    highlight = "\\x1b[0;30;47m"
    name_color = "\\x1b[0;37;44m"
    aqua = "\\x1b[0;30;46m"
    green = "\\x1b[0;30;42m"
    white = "\\x1b[0;30;47m"
    orange = "\\x1b[0;30;43m"
    red = "\\x1b[0;30;41m"
    rst_color = "\\x1b[0m"
    CRITICAL = "{{}}[FATAL  ]{{}} : ".format(red, rst_color)
    ERROR = "{{}}[ERROR  ]{{}} : ".format(red, rst_color)
    DEBUG = "{{}}[DEBUG  ]{{}} : ".format(aqua, rst_color)
    PASS = "{{}}[PASS   ]{{}} : ".format(green, rst_color)
    INFO = "{{}}[INFO   ]{{}} : ".format(white, rst_color)
    WARNING = "{{}}[WARN   ]{{}} : ".format(orange, rst_color)
    NAMETAG = "{{1}}{{0}}{{2}}".format("{project_name}", name_color, rst_color)


class AppFilter(logging.Filter):
    def filter(self, record):
        if "nametag" in dir(record):
            record.color_loglevel = record.nametag
        else:
            record.color_loglevel = getattr(PrintMsg, record.levelname)
        return True


def init_{project_name}_cli_logger(loglevel=None):
    """Initialize the {project_name} CLI logger with color formatting
    
    Args:
        loglevel (str, optional): Log level (DEBUG, INFO, etc). Defaults to None.
        
    Returns:
        logging.Logger: Configured logger instance
    """
    log = logging.getLogger(__package__)
    cli_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(color_loglevel)s%(message)s")
    cli_handler.setFormatter(formatter)
    cli_handler.addFilter(AppFilter())
    log.addHandler(cli_handler)
    if loglevel:
        loglevel = getattr(logging, loglevel.upper(), 20)
        log.setLevel(loglevel)
    return log
'''

    def _get_cli_modules_init_content(self, project_name):
        """
        Get the content for _cli_modules/__init__.py
        """
        return f'''"""
CLI modules for {project_name}
"""

from {project_name}._cli_modules.option import Option
from {project_name}._cli_modules.create import Create
'''

    def _get_cli_modules_option_content(self, project_name):
        """
        Get the content for _cli_modules/option.py
        """
        return f'''"""
Basic skeleton CLI module for {project_name}
"""

import logging

LOG = logging.getLogger(__name__)


class Option:
    """
    No Commands defined
    """

    def __init__(self):
        self.description = "Option"
        LOG.info("... ")
'''