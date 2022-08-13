import abc
from dataclasses import dataclass
from mashumaro.mixins.json import DataClassJSONMixin
from splus.models.href import Href

@dataclass
class BasePage(DataClassJSONMixin, abc.ABC):
  href: Href
  limit: int
  next: str
  offset: int
  previous: str
  total: int
  items: list