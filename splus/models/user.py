from dataclasses import dataclass
from mashumaro.mixins.json import DataClassJSONMixin

from splus.models.href import Href

@dataclass
class User(DataClassJSONMixin):
  display_name: str
  external_urls: dict
  followers: dict
  href: Href
  id: str
  images: list[dict]
  type: str
  uri: str
  country: str = None
  product: str = None
  email: str = None