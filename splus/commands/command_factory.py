import argparse
import inspect

from splus.commands.base_command import BaseCommand
from splus.commands.copy_playlist import CopyPlaylist
from splus.endpoints.factory import Endpoints

class CommandFactory():
  def __init__(self, endpoints: Endpoints):
    self._parser = argparse.ArgumentParser()
    copy = CopyPlaylist(endpoints)
    sub_parser = self._parser.add_subparsers(help=copy.help())
    copy_parser = sub_parser.add_parser(copy.name()[0])
    self._add_args(copy_parser, copy)
  
  def parse(self):
    parsed_args = self._parser.parse_args()
    func = parsed_args.func
    params = parsed_args.__dict__
    del params['func']
    func(**params) #TODO: Match non-keyword args with right argument
  
  def _add_args(self, parser : argparse.ArgumentParser, command : BaseCommand):
    sig = inspect.signature(command.run)
    for parameter_name, parameter in sig.parameters.items():
      if parameter.annotation == inspect._empty:
        parser.add_argument(parameter_name, type=parameter.annotation)
      else:
        parser.add_argument(f"--{parameter_name}", type=parameter.annotation, default=parameter.default)
    parser.set_defaults(func=BaseCommand.run)
    