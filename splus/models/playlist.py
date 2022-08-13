from dataclasses import dataclass
from typing import Generic, TypeVar
from mashumaro.mixins.json import DataClassJSONMixin
from splus.models.href import Href
from splus.models.item_page import ItemPage
from splus.models.reference import Reference

TT = TypeVar("TT", ItemPage, Reference)

@dataclass
class Playlist(Generic[TT], DataClassJSONMixin):
  collaborative: bool
  description: str
  external_urls: dict
  href: Href
  id: str
  images: list[dict]
  name: str
  owner: dict
  public: bool
  snapshot_id: str
  tracks: TT
  type: str
  uri: str
  followers: dict = None