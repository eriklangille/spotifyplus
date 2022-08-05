from flask import Flask, request
from queue import Queue
import logging

from splus import constants
from splus.auth.queue_message import QueueMessage
from splus.auth.web_server import WebServer

WEB_SERVER_TYPE = 'werkzeug'
CALLBACK_ROUTE = '/callback'

class CallbackWebServer(WebServer):
  def __init__(self, queue : Queue):
    self._app = Flask("splus", root_path=constants.ROOT_DIR)
    self._app.add_url_rule(CALLBACK_ROUTE, view_func=self._callback)
    self._queue = queue
    log = logging.getLogger(WEB_SERVER_TYPE)
    log.setLevel(logging.ERROR)
    super().__init__(self._app)
  
  def _send_message(self, message : QueueMessage):
    self._queue.put(message)
  
  def _callback(self):
    message = QueueMessage.from_request(request)
    self._send_message(message)
    if message.code is None:
      if message.error:
        return f"<html><b>ERROR</b> {message.error}</html>"
    else:
      return f"<html>Success. You can close this tab</html>"
    return f"<html>Unexpected error occured</html>"
