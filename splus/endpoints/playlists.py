from splus.endpoints.base_endpoint import BaseEndpoint
from splus.models.item_page import ItemPage
from splus.models.playlist_page import PlaylistPage
from splus.models.playlist import Playlist

class PlaylistEndpoints(BaseEndpoint):
  def get_playlist(self, playlist_id: str) -> Playlist[ItemPage]:
    res = self._session.get(f'playlists/{playlist_id}')
    return Playlist[ItemPage].from_dict(res.json())

  def get_playlist_items(self, playlist_id : str) -> ItemPage:
    res = self._session.get(f'playlists/{playlist_id}/tracks')
    return ItemPage.from_dict(res.json())
  
  def get_user_playlists(self, user_id : str) -> PlaylistPage:
    res = self._session.get(f'users/{user_id}/playlists')
    return PlaylistPage.from_dict(res.json())

  def create_playlist(self, user_id : str, name : str, public=False, collaborative=False, description : str="") -> Playlist[ItemPage]:
    res = self._session.post(f'users/{user_id}/playlists',
    json={
      "name": name,
      "public": public,
      "collaborative": collaborative,
      "description": description
    })
    return Playlist[ItemPage].from_dict(res.json())

  def add_playlist_items(self, playlist_id : str, uris : list[str], position=None) -> str:
    json = {
      "uris": uris
    }
    if position:
      json["position"] = position
    res = self._session.post(f'playlists/{playlist_id}/tracks', json=json)
    return res.json()['snapshot_id']
  
  def remove_playlist_items(self, playlist_id : str, uris: list[str], snapshot_id : str = None):
    json = {
      "tracks": list(map(lambda uri: {"uri": uri}, uris))
    }
    if snapshot_id:
      json["snapshot_id"] = snapshot_id
    res = self._session.delete(f'playlists/{playlist_id}/tracks', json=json)
    return res.json()['snapshot_id']
