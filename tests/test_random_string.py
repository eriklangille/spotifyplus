import unittest
import random

from splus.utils.random_string import random_string

class TestRandomString(unittest.TestCase):
  def setUp(self):
    random.seed(0)

  def test_random_string(self):
    self.assertEqual('yWA', random_string(3))
    self.assertEqual('cqGFzYtE', random_string(8))
