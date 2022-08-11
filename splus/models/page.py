from dataclasses import dataclass
from mashumaro.mixins.json import DataClassJSONMixin
from splus.models.href import Href

from splus.models.item import Item

@dataclass
class Page(DataClassJSONMixin):
  href: Href
  items: list[Item]
  limit: int
  next: str or None
  offset: int
  previous: str or None
  total: int