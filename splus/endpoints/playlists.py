from requests import Response

from splus.endpoints.base_endpoint import BaseEndpoint
from splus.models.page import Page


class PlaylistEndpoints(BaseEndpoint):
  def get_playlist_items(self, playlist_id : str):
    res : Response = self._session.get(f'playlists/{playlist_id}/tracks')
    result = res.json()
    return Page.from_dict(result)