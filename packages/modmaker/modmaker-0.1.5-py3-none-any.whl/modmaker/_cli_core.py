"""
CLI Core module for PyGen

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
    
    USAGE = "{prog}{global_opts}{command}{command_opts}{subcommand}{subcommand_opts}"

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
        self.args = {"global": args if args is not None else [], "commands": {}}
        self._build_args()
        self.command_parser = None
        self.subcommand_parsers = {}
        self.parser = self._build_parser(description, version)
        self.parsed_args = []

    def _build_args(self):
        """Build command and subcommand arguments"""
        for name, module in self._modules.items():
            params = self._get_params(module)
            self.args["commands"][name] = {"args": params, "subcommands": {}}
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
            kwargs = {"action": action, "help": param_help}
            if not required:
                name = name.replace("_", "-")
                kwargs.update(
                    {"required": required, "default": default, "dest": param.name}
                )
            if action == "store":
                kwargs.update({"type": val_type})
            params.append(
                [[name] if required else [f"-{name[0]}", f"--{name}"], kwargs]
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
        for line in docstring.split("\n"):
            if line.strip().startswith(f":param {param}:"):
                help_str = line.strip()[len(f":param {param}:") :].strip()
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
        for line in item.__doc__.split("\n"):
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
                help_str += f"{name}\n"
            else:
                help_str += f"{name} - {mod_help}\n"
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
            usage = self._build_usage({"command": mod})
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
                class_methods = {
                    m[0]: m[1] for m in self._get_class_methods(self._modules[mod])
                }
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
                    usage = self._build_usage({"subcommand": subcommand_name})
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
        args = args if args is not None else {}
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
                args[key] = f"{val} "
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
        return {name.lower(): cls for name, cls in member_name_class}

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
        args = {k: v for k, v in args.items() if not k.startswith("_")}
        if not subcommand:
            return command(**args)
        return getattr(command(), subcommand)(**args)