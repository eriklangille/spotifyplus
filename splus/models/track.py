from dataclasses import dataclass, field
from mashumaro.mixins.json import DataClassJSONMixin

from splus.models.album import Album
from splus.models.artist import Artist
from splus.models.href import Href

@dataclass
class Track(DataClassJSONMixin):
  album: Album
  artists: list[Artist]
  available_markets: list[str]
  disc_number: int
  duration_ms: int
  episode: bool
  explicit: bool
  external_ids: dict
  external_urls: dict
  href: Href
  id: str
  is_local: bool
  name: str
  popularity: int
  preview_url: str
  track: bool
  track_number: int
  type: str
  uri: str