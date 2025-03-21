from collections import namedtuple

from django.test import TestCase

from byuhbll_django_dry.admin import ExportActionMixin, admin_action


class AdminActionDecoratorTests(TestCase):
    def test_basic_usage(self):
        self.assertTrue(callable(admin_action))

        @admin_action
        def my_func(a, b):
            """this is my func"""
            return f'stuff{a}{b}'

        self.assertEqual(my_func.__name__, 'my_func')
        self.assertEqual(my_func.__doc__, 'this is my func')
        self.assertEqual(my_func.short_description, 'this is my func')
        self.assertEqual(my_func(1, 2), 'stuff12')


class ExportActionMixinTests(TestCase):
    def test_basic_usage(self):
        Record = namedtuple('Record', ['a', 'b', 'c'])
        data = [
            Record(1, 2, 3),
            Record('a', 'b', 'c'),
            Record(3, 2, lambda: 'something'),
        ]
        inst = ExportActionMixin()
        inst.list_display = ['a', 'b', 'c']
        method = inst.export_data
        self.assertTrue(callable(method))
        self.assertEqual(method.__doc__, 'Export selected data')
        response = method(None, data)
        self.assertEqual(response.status_code, 200)
        expected = b'a,b,c\r\n1,2,3\r\na,b,c\r\n3,2,something\r\n'
        self.assertEqual(response.content, expected)
