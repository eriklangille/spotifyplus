import threading
from werkzeug.serving import make_server
from flask import Flask

from splus import constants

class WebServer(threading.Thread):
  def __init__(self, app : Flask):
    threading.Thread.__init__(self)
    self.server = make_server('127.0.0.1', constants.DEFAULT_PORT, app)
    self.ctx = app.app_context()
    self.ctx.push()

  def run(self):
    self.server.serve_forever()

  def shutdown(self):
    self.server.shutdown()