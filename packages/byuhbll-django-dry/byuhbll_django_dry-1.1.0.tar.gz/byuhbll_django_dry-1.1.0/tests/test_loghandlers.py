import logging

from django.core import mail
from django.test import TestCase, override_settings

from byuhbll_django_dry.loghandlers import GitLabAndAdminEmailHandler

logger = logging.getLogger(__name__)
# Since this handler isn't added by default, we add it here for these tests
logger.addHandler(GitLabAndAdminEmailHandler())


class GitLabAndAdminEmailHandlerTests(TestCase):
    def setUp(self):
        from django.conf import settings

        self.settings = settings
        self.settings.DRY['GITLAB_NOTIFY_USERS'] = []

    def test_basic_usage(self):
        msg = f'Testing {self.__class__.__name__}'
        logger.error(msg)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['test@example.com'])
        self.assertEqual(mail.outbox[0].subject, f'[byuhbll_django_dry] ERROR: {msg}')

    @override_settings(ADMINS=[('Tester', 'tester@example.com')])
    def test_with_admins(self):
        msg = f'Testing {self.__class__.__name__}'
        logger.error(msg)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['tester@example.com', 'test@example.com'])
        self.assertEqual(mail.outbox[0].subject, f'[byuhbll_django_dry] ERROR: {msg}')
        self.assertTrue('@tester' not in mail.outbox[0].body)

    def test_with_gitlab_notify(self):
        # Given
        before = self.settings.DRY['GITLAB_NOTIFY_USERS']
        self.settings.DRY['GITLAB_NOTIFY_USERS'] = ['tester']
        # When
        msg = f'Testing {self.__class__.__name__}'
        logger.error(msg)
        # Then
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['test@example.com'])
        self.assertEqual(mail.outbox[0].subject, f'[byuhbll_django_dry] ERROR: {msg}')
        self.assertTrue('@tester' in mail.outbox[0].body, mail.outbox[0].body)
        self.assertEqual(len(mail.outbox[0].alternatives), 0)
        self.settings.DRY['GITLAB_NOTIFY_USERS'] = before

    def test_not_sent(self):
        # Given
        before = self.settings.DRY['GITLAB_ISSUE_CREATION_EMAIL']
        self.settings.DRY['GITLAB_ISSUE_CREATION_EMAIL'] = ''
        # When
        msg = f'Testing {self.__class__.__name__}'
        logger.error(msg)
        # Then
        self.assertEqual(len(mail.outbox), 0)
        self.settings.DRY['GITLAB_ISSUE_CREATION_EMAIL'] = before

    def test_html_sent(self):
        email_handler = GitLabAndAdminEmailHandler(include_html=True)
        logger.addHandler(email_handler)
        msg = f'Testing {self.__class__.__name__}'
        try:
            logging.getLogger(__name__).error(msg)
        finally:
            logger.removeHandler(email_handler)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].to, ['test@example.com'])
        self.assertEqual(mail.outbox[1].subject, f'[byuhbll_django_dry] ERROR: {msg}')
        self.assertEqual(len(mail.outbox[1].alternatives), 1)
        html = mail.outbox[1].alternatives[0][0]
        expected_html = f'<pre class="exception_value">{msg}</pre>'
        expected_start = '<!DOCTYPE html>'
        self.assertTrue(expected_html in html, f'{expected_html} not in {html}')
        self.assertTrue(
            html.startswith(expected_start),
            f'{html} does not start with {expected_start}',
        )
