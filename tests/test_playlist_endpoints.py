import unittest
from unittest import mock
from typing import cast

from splus.endpoints.playlists import PlaylistEndpoints
from splus.utils.spotify_session import SpotifySession
from tests.mock_requests import MockResponseBuilder, RequestType

class TestPlaylistEndpoints(unittest.TestCase):
  def setUp(self) -> None:
    mock_session = (
      MockResponseBuilder()
      .add_condition(RequestType.GET, lambda request: request.url.startswith("playlists/") and request.url.endswith("/tracks"))
        .returns_json_from_file('get_playlist_items.json')
      .add_condition(RequestType.GET, lambda request: request.url.startswith("users/") and request.url.endswith("/playlists"))
        .returns_json_from_file('get_user_playlists.json')
      .add_condition(RequestType.GET, lambda request: request.url.startswith("playlists/"))
        .returns_json_from_file('get_playlist.json')
      .add_condition(RequestType.POST, lambda request: request.url.startswith("users/") and request.url.endswith("/playlists"))
        .returns_json_from_file('get_playlist.json')
      .add_condition(RequestType.POST, lambda request: request.url.startswith("playlists/") and request.url.endswith("/tracks"))
        .returns_json_from_dict({"snapshot_id": "abcde"})
      .add_condition(RequestType.DELETE, lambda request: request.url.startswith("playlists/") and request.url.endswith("/tracks"))
        .returns_json_from_dict({"snapshot_id": "abcde"})
      .build()
    )
    self.endpoint = PlaylistEndpoints(cast(SpotifySession, mock_session))
  
  def test_get_playlist_items(self):
    playlist = self.endpoint.get_playlist_items("test")
    mock_get = cast(mock.MagicMock, self.endpoint._session.get)
    mock_get.assert_called_once()
    assert playlist.href.path == "/v1/playlists/1nYXOKEmZXnXRp31dCO031/tracks"
    assert playlist.href.path_sections[0] == "v1"

  def test_get_playlist(self):
    playlist = self.endpoint.get_playlist("test")
    mock_get = cast(mock.MagicMock, self.endpoint._session.get)
    mock_get.assert_called_once()
    assert playlist.public == False
    assert playlist.tracks.total == 6
  
  def test_get_user_playlists(self):
    user_playlists = self.endpoint.get_user_playlists("username")
    mock_get = cast(mock.MagicMock, self.endpoint._session.get)
    mock_get.assert_called_once()
    assert user_playlists.total == 39
    assert user_playlists.items[0].description == "this is a test"
  
  def test_create_playlist(self):
    test_json = {
      "name": "test",
      "public": False,
      "collaborative": False,
      "description": "this is a test"
    }
    playlist = self.endpoint.create_playlist("username", "test", description="this is a test")
    mock_post = cast(mock.MagicMock, self.endpoint._session.post)
    mock_post.assert_called_with("users/username/playlists", json=test_json)
    assert playlist.public == False
    assert playlist.tracks.total == 6

  def test_add_playlist_items(self):
    test_json = {
      "uris": ["abc", "def"],
    }
    snapshot = self.endpoint.add_playlist_items("test", ["abc", "def"])
    mock_post = cast(mock.MagicMock, self.endpoint._session.post)
    mock_post.assert_called_with("playlists/test/tracks", json=test_json)
    assert snapshot == "abcde"
  
  def test_remove_playlist_items(self):
    test_json = {
      "tracks": [
        {"uri": "abc"},
        {"uri": "def"}
      ]
    }
    snapshot = self.endpoint.remove_playlist_items("test", ["abc", "def"])
    mock_delete = cast(mock.MagicMock, self.endpoint._session.delete)
    mock_delete.assert_called_with("playlists/test/tracks", json=test_json)
    assert snapshot == "abcde"
