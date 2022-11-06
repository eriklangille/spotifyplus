import unittest
import base64
import requests
import json
from typing import cast
from unittest import mock
from splus.auth.access_token_handler import AccessTokenHandler
from splus.auth.access_token import AccessToken
from splus import constants
from tests.mock_requests import MockResponseBuilder, RequestType, TOKEN_DATA

TOKEN_DATA_STR = json.dumps(TOKEN_DATA, indent=2, sort_keys=True)

MOCK_ENCODE = "MTIzOmFiYw=="
MOCK_DECODE = "123:abc"

def mocked_base64_encode(encoded : bytes):
  return MOCK_ENCODE.encode(encoding='ascii')

class TestAccessTokenHandler(unittest.TestCase):
  def setUp(self) -> None:
    self.auth = AccessTokenHandler()
    self.auth._session = (
      MockResponseBuilder()
      .add_condition(RequestType.POST, lambda request: request.url == constants.TOKEN_URI)
        .returns_json_from_dict(TOKEN_DATA)
      .build(session=requests.Session())
    )
  
  def test_request_access_token(self):
    expected_token = AccessToken.from_dict(TOKEN_DATA)
    actual_token = self.auth._request_access_token("abcdef")

    mock_post = cast(mock.MagicMock, self.auth._session.post)
    mock_post.assert_called_once()
    assert expected_token.access_token == actual_token.access_token

  @mock.patch("base64.b64encode", side_effect=mocked_base64_encode)
  def test_generate_token_headers(self, mock : mock.Mock):
    result = self.auth._generate_token_headers()
    mock.assert_called_once()
    assert result["Authorization"] == "Basic " + MOCK_ENCODE
    assert result["Content-Type"] == "application/x-www-form-urlencoded"
  
  def test_base64_encode(self):
    result = f"{str(base64.b64encode(MOCK_DECODE.encode('ascii')), encoding='ascii')}"
    assert result == MOCK_ENCODE

  def test_auth_expired(self):
    token = AccessToken.from_dict(TOKEN_DATA)
    assert token.is_expired() == False
    token.expires_in = 0
    assert token.is_expired() == True

  @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=TOKEN_DATA_STR)
  def test_load_token(self, mock : mock.Mock):
    expected_token = AccessToken.from_dict(TOKEN_DATA)
    actual_token = self.auth.load_token()
    mock.assert_called_once()
    assert expected_token.access_token == actual_token.access_token

  @mock.patch("json.dump")
  @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=TOKEN_DATA_STR)
  def test_save_token(self, mock_op: mock.Mock, mock_dump : mock.Mock):
    expected_token = AccessToken.from_dict(TOKEN_DATA)
    self.auth.save_token(expected_token)
    mock_op.assert_called_once()
    mock_dump.assert_called_once_with(expected_token.to_dict(), fp=mock.ANY, indent=2, sort_keys=True)
