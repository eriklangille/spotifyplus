from dataclasses import dataclass
from mashumaro.mixins.json import DataClassJSONMixin
from splus.models.href import Href
from splus.models.page import Page

@dataclass
class Playlist(DataClassJSONMixin):
  collaborative: bool
  description: str
  external_urls: dict
  followers: dict
  href: Href
  id: str
  images: list[dict]
  name: str
  owner: dict
  public: bool
  snapshot_id: str
  tracks: Page
  type: str
  uri: str