"""
Logging configuration.

WARNING: Don't import settings from Django into this file.
"""

import datetime
import logging
import sys

import colorlog
import pytz


class ISO8601FormatMixin:
    """
    Used to override logging.Formatter.formatTime to return a ISO 8601 datetime in
    the format of yyyy-MM-ddTHH:mm:ss.SSS-00:00, with the timezone 'US/Mountain'
    """

    # TODO - Make configurable
    TIMEZONE = pytz.timezone('US/Mountain')

    def formatTime(self, record, datefmt=None):
        return datetime.datetime.fromtimestamp(record.created, self.TIMEZONE).isoformat(
            sep='T', timespec='milliseconds'
        )


class ISO8601Formatter(ISO8601FormatMixin, logging.Formatter):
    pass


class ISO8601ColorFormatter(ISO8601FormatMixin, colorlog.ColoredFormatter):
    pass


# DEFAULT LOGGING CONFIGURATION
config = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
    'formatters': {
        'default': {
            '()': 'byuhbll_django_dry.logging.ISO8601Formatter',
            'format': ('%(asctime)s %(levelname)s %(name)s:%(lineno)s %(message)s'),
        },
        'color': {
            '()': 'byuhbll_django_dry.logging.ISO8601ColorFormatter',
            'format': (
                '%(log_color)s%(asctime)s %(levelname)s %(name)s:%(lineno)s '
                '%(message)s%(reset)s'
            ),
            'log_colors': {
                'DEBUG': 'bold_black',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'white,bg_red',
            },
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'byuhbll_django_dry.loghandlers.GitLabAndAdminEmailHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': sys.stdout,
        },
    },
    'loggers': {'': {'level': 'INFO', 'handlers': ['console', 'mail_admins']}},
}
