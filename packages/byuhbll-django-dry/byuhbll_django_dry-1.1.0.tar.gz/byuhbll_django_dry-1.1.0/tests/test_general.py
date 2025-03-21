from django.test import TestCase


class GeneralTests(TestCase):
    def test_import(self):
        import byuhbll_django_dry

        self.assertEqual(
            byuhbll_django_dry.middleware.PingViewMiddleware.__name__,
            'PingViewMiddleware',
        )
