"""Generic views and view building blocks"""

import logging

import requests
from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.utils import timezone

logger = logging.getLogger(__name__)


class HealthCheckViewMixin:
    """
    Status health check view.

    Adds methods that follow the naming convention `check_[name]` to add new
    checks.
    """

    def get(self, request):
        """
        Calls all methods in the child class that start with `check_` and
        constructs a report of the status of external dependencies.
        """
        health = {'datetime': timezone.now()}
        methods = (m for m in dir(self) if m.startswith('check_'))

        for check_method in methods:
            key = check_method.replace('check_', '')
            health[key] = getattr(self, check_method)()

        return JsonResponse(health)

    def check_databases(self):
        response = {a: self.database_check(a) for a in connections}
        return response

    def endpoint_check(self, url, method='get', enabled=True, **kwargs):
        """
        Sends a HTTP request to an endpoint and returns a report of the status.
        """
        if not enabled:
            return {'url': url, 'status_code': -1, 'status': 'disabled'}
        else:
            resp = getattr(requests, method, 'get')(url, **kwargs)
            return {
                'url': url,
                'status_code': resp.status_code,
                'status': 'up' if resp.ok else 'down',
            }

    def database_check(self, alias, db_connections=None):
        """
        Checks the status of database connections.
        """
        from django.conf import settings

        db_connections = db_connections if db_connections else connections
        conn = db_connections[alias]
        result = {
            'engine': settings.DATABASES[alias]['ENGINE'],
            'name': settings.DATABASES[alias]['NAME'],
            'host': settings.DATABASES[alias].get('HOST', ''),
            'status': 'unknown',
        }

        try:
            conn.cursor()
        except OperationalError:
            result['status'] = 'down'
        else:
            result['status'] = 'up'

        return result
