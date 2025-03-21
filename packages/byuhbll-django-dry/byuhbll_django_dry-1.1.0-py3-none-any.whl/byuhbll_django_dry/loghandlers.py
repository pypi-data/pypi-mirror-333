"""Custom log handlers"""

from django.core.mail.message import EmailMultiAlternatives
from django.utils.log import AdminEmailHandler as OrigAdminEmailHandler


class GitLabAndAdminEmailHandler(OrigAdminEmailHandler):
    def send_mail(self, subject, message, fail_silently=False, html_message=None):
        from django.conf import settings

        gitlab_notify_users = settings.DRY['GITLAB_NOTIFY_USERS']
        gitlab_issue_creation_email = settings.DRY['GITLAB_ISSUE_CREATION_EMAIL']

        if not settings.ADMINS and not gitlab_issue_creation_email:
            return

        if gitlab_notify_users:
            notify = ' '.join(f'@{u}' for u in gitlab_notify_users)
            message = f'{notify}\n\n```\n{message}\n```'

        mail = EmailMultiAlternatives(
            f'{settings.EMAIL_SUBJECT_PREFIX}{subject}',
            message,
            settings.SERVER_EMAIL,
            [a[1] for a in settings.ADMINS] + [gitlab_issue_creation_email],
            connection=self.connection(),
        )

        if html_message:
            mail.attach_alternative(html_message, 'text/html')

        mail.send(fail_silently=fail_silently)
