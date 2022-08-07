from requests import Session
from urllib.parse import urljoin

from splus import constants
from splus.auth.access_token import AccessToken
from splus.auth.access_token_handler import AccessTokenHandler

class SpotifySession(Session):
  def __init__(self, token : AccessToken, *args, **kwargs):
    super().__init__(*args, **kwargs)
    headers = {'Authorization': f'Bearer {token.access_token}', 'Content-Type': 'application/json'}
    self._token = token
    self._base_url = constants.API_URI
    self._access_handler = AccessTokenHandler()
    self.headers = headers
  
  def request(self, method, url, *args, **kwargs):
    url = urljoin(self._base_url, url)
    if self._token.is_expired():
      self._token = self._access_handler.refresh_token(self._token)
    return super().request(method, url, *args, **kwargs)