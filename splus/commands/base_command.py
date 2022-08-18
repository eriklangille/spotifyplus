import abc
import inspect
from collections.abc import ItemsView

from splus.endpoints.factory import Endpoints

class BaseCommand(abc.ABC):
  def __init__(self, endpoints : Endpoints):
    self._endpoints = endpoints
  
  @abc.abstractmethod
  def run(self, *args, **kwargs):
    pass

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
