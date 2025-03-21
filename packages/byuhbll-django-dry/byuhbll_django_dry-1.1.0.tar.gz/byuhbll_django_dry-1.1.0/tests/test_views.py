import json
import warnings
from unittest import mock

from django.db.utils import OperationalError
from django.test import RequestFactory, TestCase
from django.views import View

from byuhbll_django_dry.views import HealthCheckViewMixin

warnings.simplefilter('ignore')


class HealthCheckViewBase(TestCase):
    def test_database_check_up(self):
        class MyDBView(HealthCheckViewMixin, View):
            pass

        request = RequestFactory().get('/status/health/')
        view = MyDBView.as_view()
        with self.settings(
            DATABASES={
                'default': {
                    'ENGINE': 'sqlite3',
                    'NAME': 'default.db',
                    'HOST': 'test',
                }
            }
        ):
            response = view(request)

        json_response = json.loads(response.content.decode('utf-8'))
        expected_db_response = {
            'engine': 'sqlite3',
            'name': 'default.db',
            'host': 'test',
            'status': 'up',
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['databases']['default'], expected_db_response)

    def test_database_check_down(self):
        conn = mock.MagicMock()

        def error():
            raise OperationalError

        conn.cursor.side_effect = error

        class MyDBView(HealthCheckViewMixin, View):
            def check_default_db(self):
                return self.database_check('default', {'default': conn})

        request = RequestFactory().get('/status/health/')
        view = MyDBView.as_view()
        with self.settings(
            DATABASES={
                'default': {
                    'ENGINE': 'sqlite3',
                    'NAME': 'default.db',
                    'HOST': 'test',
                }
            }
        ):
            response = view(request)

        json_response = json.loads(response.content.decode('utf-8'))
        expected_db_response = {
            'engine': 'sqlite3',
            'name': 'default.db',
            'host': 'test',
            'status': 'down',
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['default_db'], expected_db_response)
        conn.cursor.assert_called_once()

    def test_endpoint_check_disabled(self):
        class MyView(HealthCheckViewMixin, View):
            def check_a_url(self):
                return self.endpoint_check('asdf', enabled=False)

        request = RequestFactory().get('/status/health/')
        view = MyView.as_view()
        response = view(request)
        json_response = json.loads(response.content.decode('utf-8'))
        expected_url_response = {
            'url': 'asdf',
            'status_code': -1,
            'status': 'disabled',
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['a_url'], expected_url_response)

    @mock.patch('requests.get')
    def test_endpoint_check_enabled(self, mocked_get):
        response = mock.MagicMock()
        response.status_code = 200
        response.ok = True
        mocked_get.side_effect = lambda *a, **k: response

        class MyView(HealthCheckViewMixin, View):
            def check_a_url(self):
                return self.endpoint_check('asdf')

        request = RequestFactory().get('/status/health/')
        view = MyView.as_view()
        response = view(request)
        json_response = json.loads(response.content.decode('utf-8'))
        expected_url_response = {
            'url': 'asdf',
            'status_code': 200,
            'status': 'up',
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['a_url'], expected_url_response)

    @mock.patch('requests.get')
    def test_endpoint_check_enabled_down(self, mocked_get):
        response = mock.MagicMock()
        response.status_code = 500
        response.ok = False
        mocked_get.side_effect = lambda *a, **k: response

        class MyView(HealthCheckViewMixin, View):
            def check_a_url(self):
                return self.endpoint_check('asdf')

        request = RequestFactory().get('/status/health/')
        view = MyView.as_view()
        response = view(request)
        json_response = json.loads(response.content.decode('utf-8'))
        expected_url_response = {
            'url': 'asdf',
            'status_code': 500,
            'status': 'down',
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['a_url'], expected_url_response)
