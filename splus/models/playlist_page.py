from dataclasses import dataclass
from splus.models.playlist import Playlist
from splus.models.base_page import BasePage
from splus.models.reference import Reference

@dataclass
class PlaylistPage(BasePage):
  items: list[Playlist[Reference]]