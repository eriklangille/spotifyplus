import abc

from splus.endpoints.factory import Endpoints

class BaseCommand(abc.ABC):
  def __init__(self, endpoints : Endpoints):
    self._endpoints = endpoints
  
  @abc.abstractmethod
  def run(self):
    pass