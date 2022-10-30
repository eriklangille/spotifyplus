import argparse
import inspect
from typing import Type

from splus.commands.base_command import BaseCommand
from splus.commands.command_args import CommandArgs
from splus.commands.copy_playlist import CopyPlaylist
from splus.commands.list_playlists import ListPlaylist
from splus.endpoints.factory import Endpoints

COMMANDS : Type[BaseCommand] = [CopyPlaylist, ListPlaylist]
DESCRIPTION = "Spotify Plus. A CLI tool for doing bulk actions and power user commands."

class CommandFactory():
  def __init__(self, endpoints: Endpoints):
    self._parser = argparse.ArgumentParser()
    self.sub_parser = self._parser.add_subparsers(help=DESCRIPTION)
    for command in COMMANDS:
      self._add_command(command(endpoints))
  
  def parse(self):
    command_args = self._parser.parse_args(namespace=CommandArgs())
    command_args.run_command()
  
  def _add_command(self, command: BaseCommand):
    cmd_parser = self.sub_parser.add_parser(command.name()[0], help=command.help())
    self._add_args(cmd_parser, command)
  
  def _add_args(self, parser : argparse.ArgumentParser, command : BaseCommand):
    for parameter_name, parameter in command.get_parameters():
      if parameter.default == inspect._empty:
        parser.add_argument(parameter_name, type=parameter.annotation)
      else:
        parser.add_argument(f"--{parameter_name}", type=parameter.annotation, default=parameter.default)
    parser.set_defaults(command=command)
    