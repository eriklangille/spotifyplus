from typing import Any

from splus.commands.base_command import BaseCommand
from splus.exceptions.base_exception import BaseRequestException

class CommandArgs:
  def __init__(self):
    self._command : BaseCommand = None
    self._args : dict[str, Any] = {}

  def __setattr__(self, __name: str, __value: Any) -> None:
    if __name in ["_command", "_args"]:
      super().__setattr__(__name, __value)
      return
    if __name == "command" and isinstance(__value, BaseCommand):
      self._command = __value
      return
    self._args[__name] = __value
  
  def get_command(self) -> BaseCommand:
    return self._command
  
  def run_command(self) -> None:
    try:
      self._command.run_args(self._args)
    except BaseRequestException as err:
      print(err)
  
  def get_args(self) -> dict:
    return self._args
