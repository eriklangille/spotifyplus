import abc
import inspect
from collections.abc import ItemsView
from typing import Tuple

from splus.endpoints.factory import Endpoints

class BaseCommand(abc.ABC):
  def __init__(self, endpoints : Endpoints):
    self._endpoints = endpoints
    self._parameters: dict[str, str] = {}
  
  @abc.abstractmethod
  def run(self, *args, **kwargs):
    ...

  @abc.abstractmethod
  def help(self) -> list[str]:
    ...

  @abc.abstractmethod
  def name(self) -> Tuple[str, str]:
    ...

  def get_parameters(self) -> ItemsView[str, inspect.Parameter]:
    sig = inspect.signature(self.run)
    return sig.parameters.items()
  
  def run_args(self, kwargs : dict):
    args = {}
    for parameter_name, parameter in self.get_parameters():
      if parameter.annotation == inspect._empty:
        args[parameter_name] = kwargs[parameter_name]
        del kwargs[parameter_name]
    self.run(*args, **kwargs)
