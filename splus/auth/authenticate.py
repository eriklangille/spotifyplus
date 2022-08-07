from queue import Queue
import requests
from urllib import parse
import webbrowser
import base64

from splus import constants
from splus.auth.access_token_handler import AccessTokenHandler
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
    self._state = random_string(8)
    self._server = CallbackWebServer(self._queue)
    self._handler = AccessTokenHandler()
  
  def authenticate(self) -> AccessToken:
    self.request_permission()
    return self.get_token()
  
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
    
  def get_token(self) -> AccessToken:
    if self._code:
      return self._handler.get_token(self._code)
    raise RuntimeError("Permission must be requested first")
  
  def _check_for_message(self) -> QueueMessage:
    return self._queue.get(block=True)

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