from dataclasses import dataclass, field
from mashumaro.mixins.json import DataClassJSONMixin

@dataclass
class Album(DataClassJSONMixin):
  album_type: str
  artists: list[dict]
  available_markets: list[str]
  external_urls: dict
  href: str
  id: str
  images: list[dict]
  name: str
  release_date: str
  release_date_precision: str
  total_tracks: int
  type: str
  uri: str