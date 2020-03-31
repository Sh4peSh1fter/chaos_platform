import click
import os

from master import commands as master_commands
from db import commands as db_commands
from cli import commands as cli_commands


class ChaosSystem(object):
    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug


@click.group()
def cli_main():
    pass


cli_main.add_command(master_commands.master)
cli_main.add_command(db_commands.db)
cli_main.add_command(cli_commands.cli)





