import click

from .build import build
from .configure import configure


@click.group()
def cli():
    pass


cli.add_command(build)
cli.add_command(configure)
