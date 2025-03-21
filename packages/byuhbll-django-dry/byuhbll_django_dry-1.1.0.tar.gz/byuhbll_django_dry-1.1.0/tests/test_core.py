import unittest
from unittest import mock

from . import conman
from .utils import mocked_requests


class CoreTests(unittest.TestCase):
    def test_something(self):
        self.assertTrue(True)

    @mock.patch('requests.get', side_effect=mocked_requests(conman.SAMPLE_RESPONSE_200))
    def test_requests(self, mocked_get):
        import requests

        r = requests.get()
        self.assertEqual(r.status_code, 200)
