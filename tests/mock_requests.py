import json
from unittest import mock
from typing import Protocol, Union
from enum import Enum

from requests import Session

from splus import constants
from splus.utils.spotify_session import SpotifySession
from splus.auth.access_token import AccessToken

SAMPLE_JSON_DIR = "./tests/samples/"

TOKEN_DATA = {
  "access_token": "NgCXRK...MzYjw",
  "token_type": "Bearer",
  "scope": constants.SCOPE,
  "expires_in": 3600,
  "refresh_token": "NgAagA...Um_SHo"
}

class ResponseCallable(Protocol):
  def __call__(self, uri: str, *args, **kwargs) -> bool: ...

class RequestType(Enum):
  GET = 1
  POST = 2
  PUT = 3
  DELETE = 4
  PATCH = 5

class MockResponseBuilder:
  def __init__(self):
    self._requests : dict[RequestType, list[MockResponseCondition]] = {
      RequestType.GET: [],
      RequestType.POST: [],
      RequestType.PUT: [],
      RequestType.DELETE: [],
      RequestType.PATCH: [],
    }
  
  def add_condition(self, req_type: RequestType, condition: ResponseCallable) -> 'MockResponseCondition':
    mock_reponse_condition = MockResponseCondition(self, condition)
    self._requests[req_type].append(mock_reponse_condition)
    return mock_reponse_condition

  def _mocked_request(self, req_type: RequestType, uri : str, *args, **kwargs):
    for request in self._requests[req_type]:
      if request._condition(uri, *args, **kwargs):
        if isinstance(request._response, str):
          with open(f"{SAMPLE_JSON_DIR}{request._response}") as f:
            json_data = json.load(f)
        else:
          json_data = request._response
        json_func = mock.MagicMock(return_value=json_data)
        return MockResponseBuilder.MockResponse(json_data, json_func, 200)
    
    return MockResponseBuilder.MockResponse(None, None, 404)

  class MockResponse:
    def __init__(self, json_data, json_func, status_code):
      self.json = json_func
      self.text = json.dumps(json_data)
      self.json_data = json_data
      self.status_code = status_code
    
    def json(self):
      return self.json_data

  def _mocked_requests_get(self, uri : str, *args, **kwargs):
    return self._mocked_request(RequestType.GET, uri, *args, **kwargs)

  def _mocked_requests_post(self, uri : str, *args, **kwargs):
    return self._mocked_request(RequestType.POST, uri, *args, **kwargs)

  def _mocked_requests_put(self, uri : str, *args, **kwargs):
    return self._mocked_request(RequestType.PUT, uri, *args, **kwargs)

  def _mocked_requests_delete(self, uri : str, *args, **kwargs):
    return self._mocked_request(RequestType.DELETE, uri, *args, **kwargs)

  def _mocked_requests_patch(self, uri : str, *args, **kwargs):
    return self._mocked_request(RequestType.PATCH, uri, *args, **kwargs)
  
  def build(self, session : Session = None):
    if session:
      real = session
    else:
      real = SpotifySession(AccessToken.from_dict(TOKEN_DATA))
    real.get = mock.MagicMock(side_effect=self._mocked_requests_get)
    real.post = mock.MagicMock(side_effect=self._mocked_requests_post)
    real.put = mock.MagicMock(side_effect=self._mocked_requests_put)
    real.delete = mock.MagicMock(side_effect=self._mocked_requests_delete)
    real.patch = mock.MagicMock(side_effect=self._mocked_requests_patch)
    return real

class MockResponseCondition:
  def __init__(self, builder: MockResponseBuilder, condition : ResponseCallable):
    self._builder = builder
    self._condition = condition
    self._response : Union[str, dict] = None
  
  def returns_json_from_file(self, file_name: str):
    self._response = file_name
    return self._builder

  def returns_json_from_dict(self, dictionary: dict):
    self._response = dictionary
    return self._builder
