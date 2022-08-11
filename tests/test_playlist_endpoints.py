import unittest
import json
from unittest import mock
from splus.endpoints.playlists import PlaylistEndpoints

from splus.utils.spotify_session import SpotifySession
from splus.auth.access_token import AccessToken
from splus import constants

TOKEN_DATA = {
  "access_token": "NgCXRK...MzYjw",
  "token_type": "Bearer",
  "scope": constants.SCOPE,
  "expires_in": 3600,
  "refresh_token": "NgAagA...Um_SHo"
}

def mocked_requests_get(uri : str, *args, **kwargs):
  class MockResponse:
    def __init__(self, json_data, json_func, status_code):
      self.json = json_func
      self.text = json.dumps(json_data)
      self.json_data = json_data
      self.status_code = status_code
    
    def json(self):
      return self.json_data

  if uri.startswith("v1/playlists/") and uri.endswith("/tracks"):
    f = open("./tests/samples/get_playlist_items.json")
    json_data = json.load(f)
    json_func = mock.MagicMock(return_value=json_data)
    return MockResponse(json_data, json_func, 200)
  
  return MockResponse(None, None, 404)

def mocked_requests_session() -> mock.MagicMock:
  real = SpotifySession(AccessToken.from_dict(TOKEN_DATA))
  real.get = mock.MagicMock(side_effect=mocked_requests_get)
  return real

class TestPlaylistEndpoints(unittest.TestCase):
  def test_get_playlist_items(self):
    self.endpoint = PlaylistEndpoints(mocked_requests_session())
    playlist = self.endpoint.get_playlist_items("test")
    mock_get : mock.MagicMock = self.endpoint._session.get
    mock_get.assert_called_once()
    assert playlist.href.path == "/v1/playlists/1nYXOKEmZXnXRp31dCO031/tracks"
    assert playlist.href.path_sections[0] == "v1"