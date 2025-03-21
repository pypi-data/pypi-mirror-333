import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
_application = get_wsgi_application()


def application(environ, start_response):
    script_name = getattr(settings, 'FORCE_SCRIPT_NAME', None)
    if script_name:
        environ['SCRIPT_NAME'] = script_name
        path_info = environ['PATH_INFO']
        if path_info.startswith(script_name):
            minus_script_name = slice(len(script_name), None)
            environ['PATH_INFO'] = path_info[minus_script_name]

    scheme = environ.get('HTTP_X_SCHEME', '')
    if scheme:
        environ['wsgi.url_scheme'] = scheme

    return _application(environ, start_response)
