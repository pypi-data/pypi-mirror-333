"""
Command line interface for {{PROJECT_NAME}}.
"""

import click
from rich.console import Console

from {{PROJECT_NAME}} import __version__
from {{PROJECT_NAME}} import commands


console = Console()


@click.group()
@click.version_option(version=__version__)
def cli():
    """{{PROJECT_NAME}} - A taskcat style command-line ."""
    pass


@cli.command()
@click.option("--name", "-n", default="World", help="Name to greet")
def greet(name):
    """A Lumbergh greeting"""
    message = commands.hello(name)
    console.print(f"[bold green]{message}[/bold green]")


def main():
    """entry point for the CLI."""
    cli()
