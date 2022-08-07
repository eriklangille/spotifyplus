import requests
import base64

from splus import constants
from splus.auth.access_token import AccessToken

class AccessTokenHandler():
  def __init__(self):
    self._session = requests.session()
  
  def get_token(self, code : str) -> AccessToken:
    return self._request_access_token(code)
  
  def refresh_token(self, token : AccessToken):
    if token.is_expired():
      return self._request_refresh_token()
    return token

  def _request_access_token(self, code : str) -> AccessToken:
    headers = self._generate_token_headers()
    data = {
      "grant_type": constants.GRANT_TYPE,
      "code": code,
      "redirect_uri": constants.REDIRECT_URI
    }
    return self._post_token_request(headers, data)
  
  def _request_refresh_token(self, token : AccessToken) -> AccessToken:
    refresh_token = token.refresh_token
    headers = self._generate_token_headers()
    data = {
      "grant_type": constants.GRANT_TYPE_REFRESH,
      "refresh_token": refresh_token
    }
    return self._post_token_request(headers, data)
  
  def _post_token_request(self, headers : dict[str, str], data : dict[str, str]) -> AccessToken:
    res = self._session.post(constants.TOKEN_URI, headers=headers, data=data)
    if res.status_code == 200:
      try:
        return AccessToken.from_json(res.text)
      except:
        raise RuntimeError()
    else:
      print(res.status_code, res.raw)
      RuntimeError(res.status_code, res.raw)

  def _generate_token_headers(self) -> dict[str, str]:
    return {
      'Authorization': f'Basic {str(base64.b64encode(f"{constants.CLIENT_ID}:{constants.CLIENT_SECRET}".encode("ascii")), encoding="ascii")}',
      'Content-Type': 'application/x-www-form-urlencoded'
    }