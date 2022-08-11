from abc import ABC

from requests import Response

from splus.utils.spotify_session import SpotifySession
from splus.exceptions.bad_oauth_exception import BadOauthToken
from splus.exceptions.bad_token_exception import BadTokenException
from splus.exceptions.rate_limit_exception import RateLimitException
from splus.models.error import Error

class BaseEndpoint(ABC):
  def __init__(self, session : SpotifySession):
    self._session = session
  
  def _handle_response_error(self, res : Response):
    if res.status_code >= 200 and res.status_code <= 299:
      return res.status_code
    elif res.status_code == 401:
      raise BadTokenException(Error.from_dict(res.json()))
    elif res.status_code == 403:
      raise BadOauthToken(Error.from_dict(res.json()))
    elif res.status_code == 429:
      raise RateLimitException(Error.from_dict(res.json()))
    raise RuntimeError(res.status_code)