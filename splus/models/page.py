from dataclasses import dataclass
from mashumaro.mixins.json import DataClassJSONMixin

from splus.models.item import Item

@dataclass
class Page(DataClassJSONMixin):
  href: str
  items: list[Item]
  limit: int
  next: str or None
  offset: int
  previous: str or None
  total: int