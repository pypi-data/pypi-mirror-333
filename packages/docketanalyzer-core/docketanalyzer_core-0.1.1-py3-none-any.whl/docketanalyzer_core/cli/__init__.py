import click

from .dev import dev
from .configure import configure


@click.group()
def cli():
    """Docket Analyzer CLI"""
    pass


cli.add_command(configure)
cli.add_command(dev)
