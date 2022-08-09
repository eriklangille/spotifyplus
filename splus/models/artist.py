from dataclasses import dataclass, field
from mashumaro.mixins.json import DataClassJSONMixin

@dataclass
class Artist(DataClassJSONMixin):
  external_urls: dict
  href: str
  id: str
  name: str
  type: str
  uri: str