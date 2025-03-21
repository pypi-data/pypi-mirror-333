from django.test import TestCase
from django.test.client import Client


class TestURLS(TestCase):
    """Test various urls."""

    def setUp(self):
        """Setup data."""
        self.client = Client()

    def tearDown(self):
        """Clean up data."""

    def check_redirect(self, url, expected_location, expected_code=302):
        # Test each url
        with self.subTest(url=url):
            response = self.client.get(url, follow=False)
            self.assertRedirects(
                response,
                expected_location,
                status_code=expected_code,
                fetch_redirect_response=False,
            )

    def test_redirects(self):
        default_urls = [
            ('/admin/', 302, '/admin/login/?next=/admin/'),
            ('/login', 301, '/login/'),
        ]

        for url, code, location in default_urls:
            self.check_redirect(url, location, code)

        expected_location = (
            'https://keycloak.lib.byu.edu/realms/ces/protocol/openid-connect/auth'
        )
        expected_code = 302
        url = '/login/'
        response = self.client.get(url, follow=False)

        # The redirect to keycloak contains variable GET data, so we ignore it
        response.headers['location'] = response.headers.get('location').split('?')[0]
        self.assertRedirects(
            response,
            expected_location,
            status_code=expected_code,
            fetch_redirect_response=False,
        )
