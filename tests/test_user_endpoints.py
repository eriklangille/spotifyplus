import unittest
from unittest import mock
from typing import cast

from splus.endpoints.users import UserEndpoints
from tests.mock_requests import MockResponseBuilder, RequestType
from splus.utils.spotify_session import SpotifySession


class TestUserEndpoints(unittest.TestCase):
  def setUp(self) -> None:
    mock_session = (
      MockResponseBuilder()
      .add_condition(RequestType.GET, lambda request: request.url == "me")
        .returns_json_from_file('get_me.json')
      .build()
    )
    self.endpoint = UserEndpoints(cast(SpotifySession, mock_session))
  
  def test_get_me(self):
    user = self.endpoint.get_me()
    mock_get = cast(mock.MagicMock, self.endpoint._session.get)
    mock_get.assert_called_once()
    assert user.id == "username"
