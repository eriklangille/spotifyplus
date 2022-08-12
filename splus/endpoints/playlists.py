from requests import Response

from splus.endpoints.base_endpoint import BaseEndpoint
from splus.models.page import Page
from splus.models.playlist import Playlist


class PlaylistEndpoints(BaseEndpoint):
  def get_playlist(self, playlist_id: str):
    res = self._session.get(f'v1/playlists/{playlist_id}')
    # print(res.text)
    return Playlist.from_dict(res.json())

  def get_playlist_items(self, playlist_id : str) -> Page:
    res : Response = self._session.get(f'v1/playlists/{playlist_id}/tracks')
    return Page.from_dict(res.json())