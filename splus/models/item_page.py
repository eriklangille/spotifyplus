from dataclasses import dataclass
from splus.models.item import Item
from splus.models.base_page import BasePage

@dataclass
class ItemPage(BasePage):
  items: list[Item]