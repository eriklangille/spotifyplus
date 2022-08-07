import unittest
import requests
import base64
import json
from unittest import mock
from splus.auth.access_token import AccessToken

from splus.auth.authenticate import Authenticate
from splus import constants

TOKEN_DATA = {
  "access_token": "NgCXRK...MzYjw",
  "token_type": "Bearer",
  "scope": constants.SCOPE,
  "expires_in": 3600,
  "refresh_token": "NgAagA...Um_SHo"
}

MOCK_ENCODE = "MTIzOmFiYw=="
MOCK_DECODE = "123:abc"

def mocked_requests_post(*args, **kwargs):
  class MockResponse:
    def __init__(self, json_data, json_func, status_code):
      self.json = json_func
      self.text = json.dumps(json_data)
      self.status_code = status_code
    
    def json(self):
      return self.json_data

  if args[0] == constants.TOKEN_URI:
    json_data = TOKEN_DATA
    json_func = mock.MagicMock(return_value=AccessToken.from_dict(json_data))
    return MockResponse(json_data, json_func, 200)
  
  return MockResponse(None, 404)

def mocked_requests_session() -> mock.MagicMock:
  real = requests.session()
  real.post = mock.MagicMock(side_effect=mocked_requests_post)
  return real

def mocked_base64_encode(encoded : bytes):
  return MOCK_ENCODE.encode(encoding='ascii')

class TestAuth(unittest.TestCase):
  def setUp(self) -> None:
    self.auth = Authenticate()
    self.auth._session = mocked_requests_session()
    self.auth._server.start()
  
  def tearDown(self) -> None:
    self.auth._server.shutdown()

  def test_request_access_token(self):
    expected_token = AccessToken.from_dict(TOKEN_DATA)
    self.auth._request_access_token("abcdef")
    actual_token = self.auth._token

    mock_post : mock.MagicMock = self.auth._session.post
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
