import copy

from django.contrib.auth import get_user_model
from django.test import TestCase

from byuhbll_django_dry.auth import DryOIDCAuthBackend


class AuthTests(TestCase):
    def setUp(self):
        self.test_net_id = 'testuser'
        self.dry_oidc_auth = DryOIDCAuthBackend()
        self.claims = {
            'email': 'test@example.com',
            'family_name': 'Last',
            'given_name': 'First',
            'net_id': self.test_net_id,
            'library_id': '1abcdef23',
        }
        self.User = get_user_model()
        self.user = self.User.objects.create(
            username=self.test_net_id, email=self.claims.get('email')
        )

    def tearDown(self):
        self.User.objects.all().delete()

    def test_create_user(self):
        self.assertEqual(1, len(self.User.objects.all()))

        claims_copy = copy.copy(self.claims)
        claims_copy['net_id'] = 'testuser2'
        created_user = self.dry_oidc_auth.create_user(claims_copy)
        fetched_user = self.User.objects.get(username=claims_copy.get('net_id'))
        self.assertEqual(created_user, fetched_user)

    def test_update_user(self):
        user_count = len(self.User.objects.all())
        user = self.dry_oidc_auth.update_user(self.user, self.claims)

        self.assertEqual(user.username, self.test_net_id)
        self.assertEqual(user.library_id, '1abcdef23')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'First')
        self.assertEqual(user.last_name, 'Last')
        self.assertEqual(user_count, len(self.User.objects.all()))

    def test_update_user_missing_net_id(self):
        claims_copy = copy.copy(self.claims)
        del claims_copy['net_id']

        user = self.dry_oidc_auth.update_user(self.user, claims_copy)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'test')

    def test_get_userinfo(self):
        payload = self.claims
        user_info = self.dry_oidc_auth.get_userinfo('access', 'identity', payload)
        self.assertEqual(payload, user_info)

    def test_filter_users_by_claims(self):
        users = self.dry_oidc_auth.filter_users_by_claims(self.claims)
        self.assertEqual(users[0], self.user)

    def test_filter_users_by_missing_claims(self):
        empty_claims = {}
        users = self.dry_oidc_auth.filter_users_by_claims(empty_claims)
        self.assertEqual(len(users), 0)

    def test_describe_user_by_claims(self):
        description = self.dry_oidc_auth.describe_user_by_claims(self.claims)
        expected = f'net_id {self.user.username} and email {self.user.email}'
        self.assertEqual(description, expected)
