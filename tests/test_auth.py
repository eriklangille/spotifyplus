import unittest
from unittest import mock

from splus.auth.access_token import AccessToken
from splus.auth.authenticate import Authenticate
from splus import constants

from .test_access_token_handler import mocked_requests_session

class TestAuth(unittest.TestCase):
  def setUp(self) -> None:
    self.auth = Authenticate()
    self.auth._session = mocked_requests_session()
    self.auth._server.start()
  
  def tearDown(self) -> None:
    self.auth._server.shutdown()

  ## TODO: Tests for request_permission
