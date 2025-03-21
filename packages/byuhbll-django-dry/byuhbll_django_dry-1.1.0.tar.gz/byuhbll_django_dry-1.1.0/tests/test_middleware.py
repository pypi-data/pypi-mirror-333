from unittest.mock import MagicMock

from django.test import TestCase

from byuhbll_django_dry.middleware import PingViewMiddleware


class PingViewMiddlewareTests(TestCase):
    def test_ping_endpoint(self):
        request = MagicMock()
        request.path = 'status/ping'
        get_response = MagicMock()
        get_response.return_value = 'CALLED'

        middle = PingViewMiddleware(get_response)
        response = middle(request)
        self.assertNotEqual(response, 'CALLED')
        self.assertEqual(response.status_code, 200)
        get_response.assert_not_called()

        # trailing slash
        request.path = 'status/ping/'
        middle = PingViewMiddleware(get_response)
        response = middle(request)
        self.assertNotEqual(response, 'CALLED')
        self.assertEqual(response.status_code, 200)
        get_response.assert_not_called()

        # leading and trailing slash
        request.path = '/status/ping/'
        middle = PingViewMiddleware(get_response)
        response = middle(request)
        self.assertNotEqual(response, 'CALLED')
        self.assertEqual(response.status_code, 200)
        get_response.assert_not_called()

    def test_non_ping_endpoint(self):
        request = MagicMock()
        request.path = '/something'
        get_response = MagicMock()
        get_response.return_value = 'CALLED'

        middle = PingViewMiddleware(get_response)
        response = middle(request)
        self.assertEqual(response, 'CALLED')
        get_response.assert_called_once_with(request)
