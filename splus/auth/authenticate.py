from queue import Queue
import requests
from urllib import parse
import webbrowser
import base64

from splus import constants
from splus.auth.callback_web_server import CallbackWebServer
from splus.auth.queue_message import QueueMessage
from splus.utils.random_string import random_string
from splus.auth.access_token import AccessToken

WEB_OPEN_TAB = 2

class Authenticate:
  def __init__(self):
    self._queue = Queue(2)
    self._session = requests.session()
    self._code : str = None
    self._token : AccessToken = None
    self._state = random_string(8)
    self._server = CallbackWebServer(self._queue)
  
  def request_permission(self):
    self._server.start()
    webbrowser.open(f"{constants.AUTH_URI}{self._generate_auth_data()}", new=WEB_OPEN_TAB)
    message = self._check_for_message()
    if message.state != self._state:
      raise RuntimeError("State mismatch")
    if message.success:
      self._server.shutdown()
      self._code = message.code
    else:
      raise RuntimeError(message.error)
  
  def get_token(self):
    ### TODO: refresh only when expired
    if self._token:
      self._request_refresh_token()
    else:
      self._request_access_token(self._code)
    return self._token

  def _check_for_message(self) -> QueueMessage:
    return self._queue.get(block=True)

  def _request_access_token(self, code : str) -> None:
    headers = self._generate_token_headers()
    data = {
      "grant_type": constants.GRANT_TYPE,
      "code": code,
      "redirect_uri": constants.REDIRECT_URI
    }
    self._post_token_request(headers, data)
  
  def _request_refresh_token(self):
    refresh_token = self._token.refresh_token
    headers = self._generate_token_headers()
    data = {
      "grant_type": constants.GRANT_TYPE_REFRESH,
      "refresh_token": refresh_token
    }
    self._post_token_request(headers, data)
  
  def _post_token_request(self, headers : dict[str, str], data : dict[str, str]) -> None:
    res = self._session.post(constants.TOKEN_URI, headers=headers, data=data)
    if res.status_code == 200:
      try:
        self._token : AccessToken = AccessToken.from_json(res.text)
      except:
        print("uh oh")
    else:
      print(res.status_code, res.raw)

  def _generate_token_headers(self) -> dict[str, str]:
    return {
      'Authorization': f'Basic {str(base64.b64encode(f"{constants.CLIENT_ID}:{constants.CLIENT_SECRET}".encode("ascii")), encoding="ascii")}',
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  
  def _generate_auth_data(self) -> dict[str, str]:
    return self._encode_url({
      "response_type": constants.RESPONSE_TYPE,
      "client_id": constants.CLIENT_ID,
      "scope": constants.SCOPE,
      "redirect_uri": constants.REDIRECT_URI,
      "state": self._state
    })

  def _encode_url(self, data: dict) -> str:
    return parse.urlencode(data)