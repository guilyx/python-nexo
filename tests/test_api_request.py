import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import unittest
import nexo


class ApiTestFixture(unittest.TestCase):
    def setUp(self):
        self.client = nexo.Client("", "")

    def test_test(self):
        assert True
