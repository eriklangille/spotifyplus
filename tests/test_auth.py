import unittest
from unittest import mock

from splus.auth.access_token import AccessToken
from splus.auth.authenticate import Authenticate


class TestAuth(unittest.TestCase):
  def setUp(self) -> None:
    self.auth = Authenticate()
    self.auth._session = None
    self.auth._server.start()
  
  def tearDown(self) -> None:
    self.auth._server.shutdown()

  ## TODO: Tests for request_permission
  def test_1(self):
    pass
