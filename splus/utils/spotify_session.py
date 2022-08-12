from requests import Session, Response
from urllib.parse import urljoin

from splus import constants
from splus.auth.access_token import AccessToken
from splus.auth.access_token_handler import AccessTokenHandler

from splus.exceptions.bad_oauth_exception import BadOauthToken
from splus.exceptions.bad_token_exception import BadTokenException
from splus.exceptions.rate_limit_exception import RateLimitException
from splus.models.error import Error

class SpotifySession(Session):
  def __init__(self, token : AccessToken, *args, **kwargs):
    super().__init__(*args, **kwargs)
    headers = {'Authorization': f'Bearer {token.access_token}', 'Content-Type': 'application/json'}
    self._token = token
    self._base_url = constants.API_URI
    self._access_handler = AccessTokenHandler()
    self.headers = headers

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
  
  def request(self, method, url, *args, **kwargs):
    url = urljoin(self._base_url, url)
    if self._token.is_expired():
      self._token = self._access_handler.refresh_token(self._token)
    response = super().request(method, url, *args, **kwargs)
    self._handle_response_error(response)
    return response